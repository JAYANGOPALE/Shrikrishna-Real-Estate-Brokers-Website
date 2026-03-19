from datetime import datetime
from database.db import db

class Property(db.Model):
    __tablename__ = 'properties'

    property_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bhk = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False) # In sq ft
    listing_type = db.Column(db.String(20), nullable=False) # Rent, Sale
    property_type = db.Column(db.String(50), nullable=False) # Apartment, Villa, Plot
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Submitted by this user
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.owner_id'), nullable=True) # Optional for admin properties
    is_featured = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True) # True for Admin listings, False for hidden seller submissions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship('PropertyImage', backref='property', lazy=True, cascade="all, delete-orphan")
    inquiries = db.relationship('Inquiry', backref='property', lazy=True)
    user = db.relationship('User', backref='properties', lazy=True)

# Import related models to ensure they are registered with SQLAlchemy
from models.property_images_model import PropertyImage
from models.inquiry_model import Inquiry
