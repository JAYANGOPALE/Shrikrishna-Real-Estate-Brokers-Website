from database.db import db

class PropertyImage(db.Model):
    __tablename__ = 'property_images'

    image_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)

from models.property_model import Property
