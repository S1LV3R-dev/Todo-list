from flask import Blueprint, request, jsonify, current_app
import jwt.exceptions
from models import db, Task, User
from datetime import datetime
import jwt


tasks_bp = Blueprint('tasks', __name__)

def get_task_by_id(id):
    return db.session.query(Task).filter_by(id=id).first()

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


def decode_token(token):
    """Helper function to decode JWT token."""
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"]), None, 200
    except jwt.ExpiredSignatureError:
        return None, 'Token expired!', 419
    except jwt.InvalidTokenError:
        return None, 'Invalid token!', 401

@tasks_bp.before_request
def auth():
    """Middleware to authenticate requests."""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'result': False, 'message': 'This page requires authorization'}), 401
    token = token.split(" ")[1] if len(token.split(" ")) > 1 else ''
    dec_token, error, status_code = decode_token(token)
    if error:
        return jsonify({'result': False, 'message': error}), status_code
    username = dec_token['sub']
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        user_id = request.json['user_id']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'result': False, 'message': "This user does not exist"}), 401
    if str(user.id) != str(user_id):
        return jsonify({'result': False, 'message': "Wrong user id", 'user_id': user.id}), 403

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
    
@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id', type=int)
    task_list = fetch_tasks(user_id)
    if task_list:
        return jsonify({'tasks': task_list})
    else:
        return jsonify({'tasks': []})

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