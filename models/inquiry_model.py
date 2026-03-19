from datetime import datetime
from database.db import db

class Inquiry(db.Model):
    __tablename__ = 'inquiries'

    inquiry_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, contacted, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='inquiries')

from models.property_model import Property
from models.user_model import User
