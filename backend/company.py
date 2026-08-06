from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, cache
from models import User, Company, Job, Application

company_bp = Blueprint('company', __name__)

def get_current_company(user_id):
    company = Company.query.filter_by(user_id = user_id).first()
    return company

@company_bp.route('/company/dashboard', methods=['GET'])
@jwt_required()
def company_dashbaord():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user:
        return jsonify({'message': 'User not found'}), 404

    if current_user.role != 'company':
        return jsonify({'message': 'Company access required'}), 403
    
    company = get_current_company(current_user_id)

    if not company or not company.is_approved:
        return jsonify({'message': 'Company not approved yet'}), 403
    
    total_jobs = Job.query.filter_by(company_id = company.id).count()
    total_applications = Application.query.join(Job).filter(Job.company_id == company.id).count()

    return jsonify({
        'company_name': company.name,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'is_approved': company.is_approved
    }), 200

@company_bp.route('/company/jobs', methods=['POST'], endpoint='create_job')
@jwt_required()
def create_job():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'company':
        return jsonify({'message': 'Company access required'}), 403
    
    company = get_current_company(current_user_id)

    if not company or not company.is_approved:
        return jsonify({'message': 'Company not approved yet'}), 403
    
    data = request.get_json() or {}

    if not data.get('title'):
        return jsonify({'message': 'Job title is required'}), 400

    from datetime import datetime
    
    job = Job(
        company_id = company.id,
        title = data['title'],
        description = data.get('description', ''),
        skills_required = data.get('skills_required', ''),
        salary = data.get('salary', 0),
        location = data.get('location', ''),
        minimum_cgpa = (
            float(data['minimum_cgpa'])
            if data.get('minimum_cgpa')
            else None
        ),
        eligible_branch = data.get('eligible_branch'),
        eligible_year = (
            int(data['eligible_year'])
            if data.get('eligible_year')
            else None
        ),
        application_deadline = (
            datetime.fromisoformat(data['application_deadline'])
            if data.get('application_deadline')
            else None
        ),
        status = 'pending'
    )
    db.session.add(job)
    db.session.commit()

    cache.delete('admin_stats')

    return jsonify({'message': 'Job posted successfully, awaiting admin approval'}), 201

@company_bp.route('/company/jobs/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'company':
        return jsonify({'message': 'Company access required'}), 403

    company = get_current_company(current_user_id)

    if not company or not company.is_approved:
        return jsonify({'message': 'Company not approved yet'}), 403
    job = Job.query.get(job_id)

    if not job or job.company_id != company.id:
        return jsonify({'message': 'job not found'})

    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'message': 'Job title is required'}), 400

    from datetime import datetime

    job.title = data['title']
    job.description = data.get('description', '')
    job.skills_required = data.get('skills_required', '')
    job.salary = data.get('salary', 0)
    job.location = data.get('location', '')

    job.minimum_cgpa = (
        float(data['minimum_cgpa'])
        if data.get('minimum_cgpa')
        else None
    )
    job.application_deadline = (
        datetime.fromisoformat(data['application_deadline'])
        if data.get('application_deadline')
        else None 
    )
    job.status = 'pending'
    db.session.commit()
    cache.delete('admin_stats')
    return jsonify({
        'message': 'Placement drive updated successfully. Awaiting admin approval.'
    }), 200

@company_bp.route('/company/jobs', methods=['GET'], endpoint='get_company_jobs')
@jwt_required()
def get_company_jobs():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'company':
        return jsonify({'message': 'Company access required'}), 403
    
    company = get_current_company(current_user_id)

    if not company or not company.is_approved:
        return jsonify({'message': 'Company not approved yet'}), 403
    
    jobs = Job.query.filter_by(company_id=company.id).all()

    result=[]
    for job in jobs:
        result.append({
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'skills_required': job.skills_required,
            'salary': job.salary,
            'location': job.location,
            'minimum_cgpa': job.minimum_cgpa,
            'eligible_branch': job.eligible_branch,
            'eligible_year': job.eligible_year,
            'application_deadline': (
                job.application_deadline.isoformat()
                if job.application_deadline
                else ''
            ),
            'status': job.status,
            'total_applications': len(job.applications)
        })
    return jsonify(result), 200

@company_bp.route('/company/jobs/<int:job_id>/applications', methods=['GET'])
@jwt_required()
def get_job_applications(job_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'company':
        return jsonify({'message': 'Company access required'}), 403
    
    company = get_current_company(current_user_id)
    job = Job.query.get(job_id)

    if not job or job.company_id != company.id:
        return jsonify({'message': 'Job not found'}), 404
    
    applications = Application.query.filter_by(job_id=job_id).all()

    result = []
    for app in applications:
        result.append({
            'id': app.id,
            'student_name': app.student.full_name,
            'student_email': app.student.user.email,
            'skills': app.student.skills,
            'education': app.student.education,
            'status': app.status,
            'applied_at': app.applied_at.strftime('%Y-%m-%d')
        })
    return jsonify(result), 200

@company_bp.route('/company/applications/<int:app_id>/status', methods=['PUT'])
@jwt_required()
def update_application_status(app_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'company':
        return jsonify({'message': 'Company access required'}), 403
    
    company = get_current_company(current_user_id)
    if not company or not company.is_approved:
            return jsonify({
                'message': 'Company not approved'
            }), 403
    data = request.get_json() or {}

    application = Application.query.get(app_id)

    if not application:
        return jsonify({'message': 'Application not found'}), 404
    
    if application.job.company_id != company.id:
        return jsonify({'message': 'Unauthorized'}), 403 
    
    valid_statuses = ['shortlisted', 'interview', 'selected', 'rejected']
    new_status = data.get('status')

    if new_status not in valid_statuses:
        return jsonify({
            'message': 'Invalid status'
        }), 400

    current_status = application.status

    allowed_transitions = {

        'applied': ['shortlisted', 'rejected'],
        'shortlisted': ['interview', 'rejected'],
        'interview': ['selected', 'rejected'],
        'selected': [],
        'rejected':[]
    }
    if new_status not in allowed_transitions.get(current_status, []):
        return jsonify({
            'message': f'Cannot change status from {current_status} to {new_status}'
        }), 400
    
    
    
    if new_status == 'selected':
        from models import Placement

        existing_placement = Placement.query.filter_by(
            application_id = application.id
        ).first()

        if not existing_placement:

            placement = Placement(
                application_id = application.id,
                student_id = application.student_id,
                company_id = application.job.company_id,
                salary = application.job.salary
            )
            db.session.add(placement)

    application.status = new_status
    application.notified = False
    db.session.commit()

    return jsonify({'message': 'Application status updated successfully'}), 200

@company_bp.route('/company/jobs/<int:job_id>/status', methods=['PUT'])
@jwt_required()
def update_job_status(job_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'company':
        return jsonify({'message': 'Company access required'}), 403
    
    company = get_current_company(current_user_id)
    data = request.get_json() or {}

    job = Job.query.get(job_id)

    if not job or job.company_id != company.id:
        return jsonify({'message': 'Job not found'}), 404
    
    valid_statuses = ['approved', 'closed']

    if data.get('status') not in valid_statuses:
        return jsonify({'message': 'Invalid status'}), 400
    
    job.status = data['status']
    db.session.commit()

    return jsonify({'message': 'Job status updated successfully'}), 200

@company_bp.route('/company/applications/<int:app_id>/interview', methods=['PUT'])
@jwt_required()
def schedule_interview(app_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'company':
        return jsonify({'message': 'Company access required'}), 403
    
    company = get_current_company(current_user_id)

    if not company or not company.is_approved:
        return jsonify({
            'message': 'Company not approved'
        }), 403

    application = Application.query.get(app_id)

    if not application:
        return jsonify({'message': 'Application not found'}), 404

    if application.job.company_id != company.id:
        return jsonify({
            'message': 'unauthorized'
        }), 403
    
    if application.status != 'shortlisted':
        return jsonify({'message': 'Only shortlisted candidates can be scheduled for interview'}), 400

    data = request.get_json() or {}

    from datetime import datetime
    from models import Interview

    interview_date = datetime.fromisoformat(
        data['interview_date']
    )

    interview = Interview(
        application_id = application.id,
        interview_date = interview_date,
        mode = data.get('mode', 'online'),
        meeting_link = data.get('meeting_link')
    )

    db.session.add(interview)

    
    application.status = 'interview'
    application.notified = False
    db.session.commit()

    return jsonify({'message': 'Interview scheduled successfully'}), 200
    