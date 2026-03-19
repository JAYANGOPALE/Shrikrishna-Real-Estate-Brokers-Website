from flask_jwt_extended import get_jwt_identity
from models.user_model import User

def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.is_admin
