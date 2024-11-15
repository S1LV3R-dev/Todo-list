from flask import Blueprint, request, jsonify, current_app
from models import db, User
import hashlib
from datetime import datetime, timedelta
import jwt

users_bp = Blueprint('users', __name__)

#adds user - registration
@users_bp.route('/add_user', methods=['POST'])
def add_user():
    username = request.json['username']
    password = request.json['password']
    user_exists = User.query.filter_by(username=username).first()
    if user_exists:
        return jsonify({"result": False, "message": "User already exists"}), 400
    password_hash = hashlib.sha256(f"{username}:{password}".encode()).hexdigest()
    new_user = User(username=username, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    payload = {
        'sub': username,
        'exp': datetime.now() + timedelta(hours=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({"result": True, "message": "User added successfully!", 'token': token, 'id': new_user.id})

#check if user exists and hased password from request equals hased password in database
@users_bp.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    password_hash = hashlib.sha256(f"{username}:{password}".encode()).hexdigest()
    user = User.query.filter_by(username=username).first()
    if user:
        if password_hash == user.password:
            payload = {
                'sub': username,
                'exp': datetime.now() + timedelta(hours=1)
            }
            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({"result": True, "message": "Login successful", 'token': token, 'id': user.id})
        else:
            return jsonify({'result': False, 'message': 'Invalid password'}), 401
    else:
        return jsonify({'result': False, "message": "User not found"}), 401