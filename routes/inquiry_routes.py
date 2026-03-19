from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.inquiry_service import create_inquiry
from utils.response_format import success_response, error_response

inquiry_bp = Blueprint('inquiry', __name__)

@inquiry_bp.route('/send', methods=['POST'])
@jwt_required()
def send_inquiry():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        inquiry = create_inquiry(user_id, data)
        return success_response(message="Inquiry sent successfully")
    except Exception as e:
        return error_response(str(e), 500)
