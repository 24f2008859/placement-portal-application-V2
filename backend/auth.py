from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db 
from models import User


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register/student', methods=['POST'])
def register_student():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password required'}), 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 409
    
    user = User(
        email = data['email'],
        password = data['password'],
        role = 'student'
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message':'Student registered successfully'}), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()

    if not user or user.password != data['password']:
        return jsonify({'message': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        'access_token': access_token,
        'role': user.role,
        'message': 'Login successful'
    }), 200