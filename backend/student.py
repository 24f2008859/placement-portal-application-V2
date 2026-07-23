from flask import Blueprint, request, jsonify 
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db 
from models import User, Student, Job, Application 

student_bp = Blueprint('student', __name__)

def get_current_student(user_id):
    student = Student.query.filter_by(user_id = user_id).first()
    return student 

@student_bp.route('/student/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'student':
        return jsonify({'message': 'Student access required'}), 403
    
    student = get_current_student(current_user_id)

    if not student:
        return jsonify({'message': 'Student profile not found'}), 404
    
    return jsonify({
        'id': student.id,
        'full_name': student.full_name,
        'phone': student.phone,
        'education': student.education,
        'skills': student.skills,
        'resume': student.resume,
        'email': current_user.email
    }), 200

@student_bp.route('/student/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'student':
        return jsonify({'message': 'Student access required'}), 403
    
    student = get_current_student(current_user_id)

    if not student:
        return jsonify({'message': 'Student profile not found'}), 404
    
    data = request.get_json()

    student.full_name = data.get('full_name', student.full_name)
    student.phone = data.get('phone', student.phone)
    student.education = data.get('education', student.education)
    student.skills = data.get('skills', student.skills)

    db.session.commit()

    return jsonify({'message': 'Profile updated successfully'}), 200

@student_bp.route('/student/jobs', methods=['GET'])
@jwt_required()
def get_approved_jobs():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'student':
        return jsonify({'message': 'Student access required'}), 403
    
    search = request.args.get('search', '')

    query = Job.query.filter_by(status = 'approved')

    if search:
        query = query.filter(
            db.or_(
                Job.title.contains(search),
                Job.skills_required.contains(search),
                Job.location.contains(search)
            )
        )
    
    jobs = query.all()

    result = []
    for job in jobs:
        result.append({
            'id': job.id,
            'title': job.title,
            'company': job.company.name,
            'location': job.location,
            'salary': job.salary,
            'skills_required': job.skills_required,
            'description': job.description
        })

    return jsonify(result), 200

@student_bp.route('/student/jobs/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def apply_job(job_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'student':
        return jsonify({'message': 'Student access required'}), 403

    student = get_current_student(current_user_id)

    job = Job.query.get(job_id)
    if not job or job.status != 'approved':
        return jsonify({'message': 'Job not found or not approved'}), 404

    existing_application = Application.query.filter_by(
        student_id = student.id,
        job_id = job_id
    ).first()

    if existing_application:
        return jsonify({'message':'You have already applied for this job'}), 409

    application = Application(
        student_id = student.id,
        job_id = job.id,
        status = 'applied'
    )
    db.session.add(application)
    db.session.commit()

    return jsonify({'message': 'Application submitted successfully'}), 201

@student_bp.route('/student/applications', methods=['GET'])
@jwt_required()
def get_my_application():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'student':
        return jsonify({'message': 'Student access required'}), 403

    student = get_current_student(current_user_id)

    applications = Application.query.filter_by(student_id = student.id).all()

    result = []
    for app in applications:
        result.append({
            'id': app.id,
            'job_title':app.job.title,
            'company': app.job.company.name,
            'location': app.job.location,
            'salary': app.job.salary,
            'status': app.status,
            'applied_at': app.applied_at.strftime('%Y-%m-%d'),
            'notified': app.notified
        })

    return jsonify(result), 200