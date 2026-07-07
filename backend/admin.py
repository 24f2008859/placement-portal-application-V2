from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, Company

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/companies/pending', methods=['GET'])
@jwt_required()
def get_pending_companies():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

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

    return jsonify({'message': 'Company approved successfully'}), 200