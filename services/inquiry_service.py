from models.inquiry_model import Inquiry
from database.db import db

def create_inquiry(user_id, data):
    new_inquiry = Inquiry(
        user_id=user_id,
        property_id=int(data['property_id']),
        message=data['message']
    )
    db.session.add(new_inquiry)
    db.session.commit()
    return new_inquiry

def get_all_inquiries():
    return Inquiry.query.all()

def get_inquiries_by_user(user_id):
    return Inquiry.query.filter_by(user_id=user_id).all()
