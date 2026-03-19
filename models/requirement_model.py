from datetime import datetime
from database.db import db

class UserRequirement(db.Model):
    """
    Model for storing user property requirements.
    """
    __tablename__ = 'user_requirements'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Requirement Details
    requirement_type = db.Column(db.String(50), nullable=False) # Buy / Rent / Lease
    property_type = db.Column(db.String(50), nullable=False)    # Flat / House / Land / Commercial
    location = db.Column(db.String(100), nullable=False)        # City / Area
    
    budget_min = db.Column(db.Numeric(15, 2), nullable=False)
    budget_max = db.Column(db.Numeric(15, 2), nullable=False)
    
    bhk = db.Column(db.String(20), nullable=True)               # 1BHK, 2BHK, etc.
    description = db.Column(db.Text, nullable=True)
    
    contact_preference = db.Column(db.String(50), nullable=False) # Call / Email / Both
    
    # Admin Tracking
    status = db.Column(db.String(20), default='Pending')        # Pending, Contacted, Closed
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref=db.backref('requirements', lazy=True))

    def __repr__(self):
        return f'<UserRequirement {self.id} - {self.requirement_type} in {self.location}>'
