from models.requirement_model import UserRequirement
from database.db import db
from datetime import datetime

def create_requirement(user_id, data):
    """Create a new user requirement."""
    new_req = UserRequirement(
        user_id=user_id,
        requirement_type=data.get('requirement_type'),
        property_type=data.get('property_type'),
        location=data.get('location'),
        budget_min=data.get('budget_min'),
        budget_max=data.get('budget_max'),
        bhk=data.get('bhk'),
        description=data.get('description'),
        contact_preference=data.get('contact_preference')
    )
    db.session.add(new_req)
    db.session.commit()
    return new_req

def get_user_requirements(user_id):
    """Fetch all requirements for a specific user."""
    return UserRequirement.query.filter_by(user_id=user_id).order_by(UserRequirement.created_at.desc()).all()

def get_requirement_by_id(req_id):
    """Fetch a single requirement by its ID."""
    return UserRequirement.query.get(req_id)

def update_requirement(req_id, data):
    """Update an existing requirement."""
    req = UserRequirement.query.get(req_id)
    if not req:
        return None
    
    req.requirement_type = data.get('requirement_type')
    req.property_type = data.get('property_type')
    req.location = data.get('location')
    req.budget_min = data.get('budget_min')
    req.budget_max = data.get('budget_max')
    req.bhk = data.get('bhk')
    req.description = data.get('description')
    req.contact_preference = data.get('contact_preference')
    
    db.session.commit()
    return req

def delete_requirement(req_id):
    """Delete a requirement."""
    req = UserRequirement.query.get(req_id)
    if req:
        db.session.delete(req)
        db.session.commit()
        return True
    return False

def get_all_requirements(filters=None):
    """
    Fetch all requirements with optional filtering for Admin.
    filters: dict with keys like 'location', 'property_type', 'status', 'budget_min', 'budget_max'
    """
    query = UserRequirement.query
    
    if filters:
        if filters.get('location'):
            query = query.filter(UserRequirement.location.ilike(f"%{filters['location']}%"))
        if filters.get('property_type'):
            query = query.filter_by(property_type=filters['property_type'])
        if filters.get('status'):
            query = query.filter_by(status=filters['status'])
        if filters.get('budget_min'):
            query = query.filter(UserRequirement.budget_max >= filters['budget_min'])
        if filters.get('budget_max'):
            query = query.filter(UserRequirement.budget_min <= filters['budget_max'])
            
    return query.order_by(UserRequirement.created_at.desc()).all()

def update_requirement_status(req_id, status):
    """Update the status of a requirement (Admin function)."""
    req = UserRequirement.query.get(req_id)
    if req:
        req.status = status
        db.session.commit()
        return True
    return False

def find_matching_properties(req_id):
    """
    Find properties that match a specific requirement.
    Basic logic: Match by property_type, location, and price within budget range.
    """
    from models.property_model import Property
    req = UserRequirement.query.get(req_id)
    if not req:
        return []
    
    # Simple matching logic
    matches = Property.query.filter(
        Property.property_type == req.property_type,
        Property.location.ilike(f"%{req.location}%"),
        Property.price >= req.budget_min,
        Property.price <= req.budget_max
    ).all()
    
    return matches
