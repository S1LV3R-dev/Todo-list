from flask import Blueprint, request, jsonify, current_app, g
import jwt.exceptions
from models import db, Task, User
from datetime import datetime, timedelta
import jwt


tasks_bp = Blueprint('tasks', __name__)

#helper function for fetching task by task id
def get_task_by_id(id):
    return db.session.query(Task).filter_by(id=id).first()

#helper function for fetching all tasks for user
def fetch_tasks(user_id):
    task_list_db = Task.query.filter_by(user_id=user_id).all()
    task_list = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'done': task.done,
        'created_at': task.created_at.strftime('%D %H:%M:%S')
        } for task in task_list_db]
    return task_list

#decode jwt token
def decode_token(token):
    """Helper function to decode JWT token."""
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"]), None, 200
    except jwt.ExpiredSignatureError:
        return None, None, 419
    except jwt.InvalidTokenError:
        return None, 'Invalid token!', 401

#handles cors
@tasks_bp.before_request
def handle_cors():
    origin = request.headers.get('Origin')
    
    # Allow all origins (wildcard)
    if origin:
        # Set CORS headers
        response = jsonify()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        # For OPTIONS request, return immediately
        if request.method == 'OPTIONS':
            return response

#authenticate user when trying to access tasks api
@tasks_bp.before_request
def auth():
    token = request.headers.get('Authorization')
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        user_id = request.json['user_id']
    if not token:
        return jsonify({'result': False, 'message': 'This page requires authorization'}), 401
    token = token.split(" ")[1] if len(token.split(" ")) > 1 else ''
    dec_token, error, status_code = decode_token(token)
    if str(status_code) == '419':
        user = User.query.filter_by(id=user_id).first()
        payload = {
            'sub': user.username,
            'exp': datetime.now() + timedelta(hours=1)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        g.custom_data = {'token': token}
    elif error:
        return jsonify({'result': False, 'message': error}), status_code
    else:
        username = dec_token['sub']
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'result': False, 'message': "This user does not exist"}), 401
        if str(user.id) != str(user_id):
            return jsonify({'result': False, 'message': "Wrong user id", 'user_id': user.id}), 403

#create task route
@tasks_bp.route('/create_task', methods=['POST'])
def create_task():
    data = request.get_json()
    created_at = datetime.now()
    try:
        new_task = Task(title=data['title'], description=data['description'], user_id=data['user_id'], created_at=created_at)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
            "result": True,
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "created_at": new_task.created_at.strftime('%D %H:%M:%S'),
            "message": "Task created successfully!"
        })
    except Exception as e:
        return jsonify({'result': False, 'message': str(e)})

    
#fetch all tasks
@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id', type=int)
    task_list = fetch_tasks(user_id)
    if task_list:
        return jsonify({'tasks': task_list})
    else:
        return jsonify({'tasks': []})

#update task status
@tasks_bp.route('/update', methods=['PUT'])
def update_small():
    user_id = request.json['user_id']
    task_id = request.json['task_id']
    done = request.json['done']
    task = db.session.query(Task).filter_by(id=task_id).first()  # Query the task
    if task:
        task.done = done  # Update the field value
        db.session.commit() 
    task_list = fetch_tasks(user_id)
    return jsonify({'tasks': task_list}), 200

#update task info
@tasks_bp.route('/update', methods=['POST'])
def update_full():
    data = request.get_json()
    task = get_task_by_id(data['task_id']) # Query the task
    if task:
        task.title = data['title']
        task.description = data['description']
        db.session.commit() 
    task_list = fetch_tasks(data['user_id'])
    return jsonify({'tasks': task_list}), 200

#delete task
@tasks_bp.route('/delete', methods=['DELETE'])
def delete_task():
    user_id = request.json['user_id']
    task_id = request.json['task_id']
    task = get_task_by_id(task_id)  # Query the task
    if task:
        db.session.delete(task)  # Delete task
        db.session.commit()
    task_list = fetch_tasks(user_id)
    return jsonify({'tasks': task_list}), 200

@tasks_bp.after_request
def after_request(response):
    # Inject custom data into the response (e.g., as a JSON field)
    if response.is_json:
        response_data = response.get_json()
        if response_data is not None and hasattr(g, 'custom_data'):
            response_data['token_new'] = g.custom_data['token']
            response.set_data(jsonify(response_data).data)
    return response