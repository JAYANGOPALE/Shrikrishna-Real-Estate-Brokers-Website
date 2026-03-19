from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from utils.auth_utils import is_admin
from utils.response_format import success_response, error_response
from services.owner_service import create_owner, get_all_owners
from services.property_service import create_property, update_property, delete_property
from services.inquiry_service import get_all_inquiries

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@jwt_required()
def admin_check():
    if not is_admin():
        return error_response("Admin access required", 403)

@admin_bp.route('/owner', methods=['POST'])
def add_owner():
    data = request.get_json()
    try:
        owner = create_owner(data)
        return success_response(data={'owner_id': owner.owner_id}, message="Owner added successfully")
    except Exception as e:
        return error_response(str(e), 500)

@admin_bp.route('/owners', methods=['GET'])
def get_owners():
    owners = get_all_owners()
    return success_response(data=[{
        'owner_id': o.owner_id,
        'name': o.owner_name,
        'phone': o.phone,
        'email': o.email,
        'address': o.address
    } for o in owners])

@admin_bp.route('/property', methods=['POST'])
def add_property():
    # Expecting form-data for file upload
    data = request.form
    files = request.files
    try:
        prop = create_property(data, files)
        return success_response(data={'property_id': prop.property_id}, message="Property added successfully")
    except Exception as e:
        return error_response(str(e), 500)

@admin_bp.route('/property/<int:property_id>', methods=['PUT'])
def edit_property(property_id):
    data = request.get_json()
    prop = update_property(property_id, data)
    if prop:
        return success_response(message="Property updated successfully")
    return error_response("Property not found", 404)

@admin_bp.route('/property/<int:property_id>', methods=['DELETE'])
def remove_property(property_id):
    if delete_property(property_id):
        return success_response(message="Property deleted successfully")
    return error_response("Property not found", 404)

@admin_bp.route('/inquiries', methods=['GET'])
def view_inquiries():
    inquiries = get_all_inquiries()
    result = []
    for i in inquiries:
        result.append({
            'inquiry_id': i.inquiry_id,
            'user_name': i.user.name,
            'property_title': i.property.title,
            'owner_name': i.property.owner.owner_name,
            'owner_phone': i.property.owner.phone, # Only admin sees this
            'message': i.message,
            'status': i.status,
            'created_at': i.created_at
        })
    return success_response(data=result)
