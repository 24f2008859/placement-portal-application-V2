from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, cache
from models import User, Company

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/companies/pending', methods=['GET'])
@jwt_required()
def get_pending_companies():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user:
        return jsonify({'message': 'User not found'}), 404

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    pending_companies = Company.query.filter_by(is_approved = False).all()

    result = [ ]
    for company in pending_companies:
        result.append({
            'id': company.id,
            'name': company.name,
            'industry': company.industry,
            'location': company.location,
            'email': company.user.email
        })
    return jsonify(result), 200

@admin_bp.route('/admin/companies/<int:company_id>/approve', methods=['PUT'])
@jwt_required()
def approve_company(company_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    company = Company.query.get(company_id)

    if not company:
        return jsonify({'message': 'Company not found'}), 404
    
    company.is_approved = True
    db.session.commit()

    cache.delete('admin_stats')

    return jsonify({'message': 'Company approved successfully'}), 200

@admin_bp.route('/admin/dashboard/stats', methods = ['GET'])
@jwt_required()
@cache.cached(timeout=300, key_prefix='admin_stats')
def dashboard_stats():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from models import Student, Company, Job, Application, Placement
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()
    total_placements = Placement.query.count()
    pending_jobs = Job.query.filter_by(status='pending').count()
    placed_students = Placement.query.count()
    placement_rate = round((placed_students / total_students * 100), 1) if total_students > 0 else 0

    return jsonify({
        'total_students': total_students,
        'total_companies': total_companies,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_placements': total_placements,
        'placed_students': placed_students,
        'placement_rate': placement_rate
    }), 200

@admin_bp.route('/admin/companies/<int:company_id>/remove', methods=['DELETE'])
@jwt_required()
def remove_company(company_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from models import Company
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    
    db.session.delete(company)
    db.session.commit()

    return jsonify({'message': 'Company removed successfully'}), 200

@admin_bp.route('/admin/companies/<int:company_id>/deactivate', methods=['PUT'])
@jwt_required()
def deactivate_company(company_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from models import Company
    company = Company.query.get(company_id)

    if not company:
        return jsonify({'message': 'Company not found'}), 404
    
    company.is_active = False
    db.session.commit()

    return jsonify({'message': 'Company deactivated successfully'}), 200

@admin_bp.route('/admin/companies/search', methods = ['GET'])
@jwt_required()
def search_companies():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from models import Company
    name = request.args.get('name', '')
    industry = request.args.get('industry', '')
    
    query = Company.query 

    if name:
        query = query.filter(Company.name.contains(name))
    if industry:
        query = query.filter(Company.industry.contains(industry))

    companies = query.all()

    result = []
    for company in companies:
        result.append({
            'id': company.id, 
            'name': company.name,
            'industry': company.industry,
            'location': company.location, 
            'is_approved': company.is_approved,
            'is_active': company.is_active
        })
    return jsonify(result), 200

@admin_bp.route('/admin/students/search', methods = ['GET'])
@jwt_required()
def search_students():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from models import Student
    name = request.args.get('name', '')
    student_id = request.args.get('id', '')
    branch = request.args.get('branch', '')
    graduation_year = request.args.get('graduation_year', '')

    query = Student.query

    if name:
        query = query.filter(Student.full_name.contains(name))
    if student_id:
        query = query.filter(Student.id == student_id)

    if branch:
        query = query.filter(
            Student.branch.contains(branch)
        )

    if graduation_year:
        query = query.filter(
            Student.graduation_year == graduation_year
        )

    students = query.all()

    result = []
    for student in students:
        result.append({
            'id': student.id,
            'full_name': student.full_name,
            'education': student.education,
            'skills': student.skills,
            'cgpa': student.cgpa,
            'branch': student.branch,
            'graduation_year': student.graduation_year,
            'is_active': student.is_active
        })

    return jsonify(result), 200

@admin_bp.route('/admin/students/<int:student_id>/deactivate', methods=['PUT'])
@jwt_required()
def deactivate_student(student_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from models import Student
    student = Student.query.get(student_id)

    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    student.is_active = False
    db.session.commit()

    return jsonify({'message': 'Student deactivated successfully'}), 200

@admin_bp.route('/admin/jobs', methods=['GET'])
@jwt_required()
def get_all_jobs():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from models import Job
    jobs = Job.query.all()

    result = []
    for job in jobs:
        result.append({
            'id': job.id,
            'title': job.title,
            'company': job.company.name,
            'location': job.location,
            'salary': job.salary,
            'status': job.status,
            'skills_required': job.skills_required
        })

    return jsonify(result), 200

@admin_bp.route('/admin/jobs/<int:job_id>/approve', methods=['PUT'])
@jwt_required()
def approve_job(job_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from models import Job 
    job = Job.query.get(job_id)

    if not job:
        return jsonify({'message': 'Job not found'}), 404
    
    job.status = 'approved'
    db.session.commit()

    cache.delete('approved_jobs')
    cache.delete('admin_stats')

    return jsonify({'message': 'Job approved successfully'}), 200


@admin_bp.route('/admin/jobs/<int:job_id>/remove', methods=['DELETE'])
@jwt_required()
def remove_job(job_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from models import Job 
    job = Job.query.get(job_id)

    if not job:
        return jsonify({'message': 'Job not found'}), 404
    
    db.session.delete(job)
    db.session.commit()

    return jsonify({'message': 'Job removed successfully'}), 200

@admin_bp.route('/admin/applications', methods=['GET'])
@jwt_required()
def get_all_applications():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from models import Application
    applications = Application.query.all()

    result = []
    for application in applications:
        result.append({
            'id': application.id,
            'student': application.student.full_name,
            'job': application.job.title,
            'company': application.job.company.name,
            'status': application.status,
            'applied_at': application.applied_at.strftime('%Y-%m-%d')
        })

    return jsonify(result), 200

@admin_bp.route('/admin/students/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_profile(student_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    from models import Student
    student = Student.query.get(student_id)

    if not student:
        return jsonify({'message': 'Student not found'}), 404

    return jsonify({
        'id': student.id,
        'full_name': student.full_name,
        'email': student.user.email,
        'education': student.education,
        'skills': student.skills,
        'resume': student.resume,
        'cgpa': student.cgpa,
        'branch': student.branch,
        'graduation_year': student.graduation_year,
        'is_active': student.is_active
    }), 200

@admin_bp.route('/admin/students/<int:student_id>/applications', methods=['GET'])
@jwt_required()
def get_student_applications(student_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    from models import Student, Application 
    student = Student.query.get(student_id)

    if not student:
        return jsonify({'message': 'Student not found'}), 404

    applications = Application.query.filter_by(student_id=student_id).all()

    result = []
    for app in applications:
        result.append({
            'id': app.id,
            'job_title': app.job.title,
            'company': app.job.company.name,
            'status': app.status,
            'applied_at': app.applied_at.strftime('%Y-%m-%d')
        })
    return jsonify(result), 200

@admin_bp.route('/admin/trigger-reminders', methods=['POST'])
@jwt_required()
def trigger_reminders():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    from tasks import send_interview_reminders
    send_interview_reminders.delay()

    return jsonify({'message': 'Interview reminders triggered successfully'}), 200

@admin_bp.route('/admin/generate-report', methods=['POST'])
@jwt_required()
def generate_report():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    from tasks import send_monthly_report
    send_monthly_report.delay()
    
    return jsonify({'message': 'Monthly report generation triggered successfully'}), 200

@admin_bp.route('/admin/charts/data', methods=['GET'])
@jwt_required()
def get_chart_data():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    from models import Application, Company, Job

    #Application per company
    companies = Company.query.filter_by(is_approved=True).all()
    company_labels = []
    company_data = []

    for company in companies:
        total = Application.query.join(Job).filter(Job.company_id == company.id).count()
        company_labels.append(company.name)
        company_data.append(total)

    # Application status distribution
    statuses = ['applied', 'interview', 'selected', 'rejected']
    status_data = []
    for status in statuses:
        count = Application.query.filter_by(status=status).count()
        status_data.append(count)

    return jsonify({
        'company_labels': company_labels,
        'company_data': company_data,
        'status_labels': statuses,
        'status_data': status_data
    }), 200