from flask import Blueprint, request
from models.user_model import User, GlobalSetting
from database.db import db
from flask_jwt_extended import create_access_token
from utils.response_format import success_response, error_response
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return error_response("Email already registered", 400)
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone', '')
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return success_response(message="User registered successfully")

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        # Track last login
        last_user_setting = GlobalSetting.query.filter_by(key='last_logged_in_user').first()
        if not last_user_setting:
            last_user_setting = GlobalSetting(key='last_logged_in_user')
            db.session.add(last_user_setting)
        
        last_user_setting.value = user.name
        user.last_login_at = datetime.utcnow()
        db.session.commit()

        access_token = create_access_token(identity=user.id)
        return success_response(data={'access_token': access_token, 'is_admin': user.is_admin, 'name': user.name}, message="Login successful")
    
    return error_response("Invalid credentials", 401)

@auth_bp.route('/last_user', methods=['GET'])
def get_last_user():
    setting = GlobalSetting.query.filter_by(key='last_logged_in_user').first()
    return success_response(data={'last_user': setting.value if setting else "None"})
