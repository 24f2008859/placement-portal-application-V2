from flask import Blueprint, jsonify
from app import db 

public_bp = Blueprint('public', __name__)

@public_bp.route('/public/stats', methods=['GET'])
def get_public_stats():
    from models import Student, Company, Job 

    total_students = Student.query.count()
    total_companies = Company.query.filter_by(is_approved=True).count()
    total_jobs = Job.query.filter_by(status='approved').count()

    return jsonify({
        'total_students': total_students,
        'total_companies': total_companies,
        'total_jobs': total_jobs
    }), 200

@public_bp.route('/public/branches', methods=['GET'])
def get_branches():
    branches = [
        "Computer Science",
        "Data Science",
        "Artificial Intelligence",
        "Information technology",
        "Electronics",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering"
    ]
    return jsonify(branches), 200

@public_bp.route('/public/degrees', methods=['GET'])
def get_degrees():
    degrees = [
        "B.Tech",
        "B.E.",
        "BS",
        "M.Tech"
    ]
    return jsonify(degrees), 200