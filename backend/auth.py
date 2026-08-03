from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import db 
from models import User


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register/student', methods=['POST'])
def register_student():
    data = request.get_json() or {}

    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password required'}), 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 409

    
    try:    
        user = User(
            email = data['email'],
            password = generate_password_hash(data['password']),
            role = 'student'
        )
        db.session.add(user)
        db.session.flush()
        from models import Student
        student = Student(
            user_id = user.id,
            full_name = data.get('full_name', ''),
            education = data.get('education', ''),
            skills = data.get('skills', ''),
            cgpa = data.get('cgpa'),
            branch = data.get('branch'),
            graduation_year = data.get('graduation_year')
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({'message':'Student registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed'}), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    if user.role == 'student':
        from models import Student

        student = Student.query.filter_by(
            user_id=user.id
        ).first()

        if student and not student.is_active:
            return jsonify({
                'message':'Student account deactivated'
            }), 403
    
    if user.role == 'company':
        from models import Company
        company = Company.query.filter_by(user_id = user.id).first()
        if not company:
            return jsonify({
                'message': 'Company profile not found'
            }),404

        if not company.is_active:
            return jsonify({
                'message': 'Company account deactivated'
            }), 403

        if not company.is_approved:
            return jsonify({
                'message': 'Company account pending admin approval'
            }), 403
    
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        'access_token': access_token,
        'role': user.role,
        'email': user.email,
        'message': 'Login successful'
    }), 200

@auth_bp.route('/auth/register/company', methods=['POST'])
def register_company():
    data = request.get_json() or {}

    if not data:
        return jsonify({'message': "No data provided"}), 400
    
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'message': 'Email, password and company name required'}), 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 409

    try:    
        user = User(
            email = data['email'],
            password = generate_password_hash(data['password']),
            role = 'company'
        )
        db.session.add(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({
            'message': 'Company registration failed'
        }), 500

    from models import Company
    company = Company(
        user_id = user.id, 
        name = data['name'],
        industry = data.get('industry', ''),
        location = data.get('location', ''),
        website = data.get('website', '')
    )

    try:
        db.session.add(company)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({
            'message': 'Company profile creation failed'
        }), 500

    return jsonify({'message': 'Company registered successfully, awaiting admin approval'}), 201
