from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
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
        password = generate_password_hash(data['password']),
        role = 'student'
    )
    db.session.add(user)
    db.session.commit()
    from models import Student
    student = Student(
        user_id = user.id,
        full_name = data.get('full_name', ''),
        phone = data.get('phone', ''),
        education = data.get('education', ''),
        skills = data.get('skills', '')
    )
    db.session.add(student)
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

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    if user.role == 'company':
        from models import Company
        company = Company.query.filter_by(user_id = user.id).first()
        if not company or not company.is_approved:
            return jsonify({'message': 'Company account pending admin approval'}), 403
    
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        'access_token': access_token,
        'role': user.role,
        'email': user.email,
        'message': 'Login successful'
    }), 200

@auth_bp.route('/auth/register/company', methods=['POST'])
def register_company():
    data = request.get_json()

    if not data:
        return jsonify({'message': "No data provided"}), 400
    
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'message': 'Email, password and company name required'}), 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 409
    
    user = User(
        email = data['email'],
        password = generate_password_hash(data['password']),
        role = 'company'
    )
    db.session.add(user)
    db.session.commit()

    from models import Company
    company = Company(
        user_id = user.id, 
        name = data['name'],
        industry = data.get('industry', ''),
        location = data.get('location', '')
    )
    db.session.add(company)
    db.session.commit()

    return jsonify({'message': 'Company registered successfully, awaiting admin approval'}), 201
