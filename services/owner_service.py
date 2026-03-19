from models.owner_model import Owner
from database.db import db

def create_owner(data):
    new_owner = Owner(
        owner_name=data['owner_name'],
        phone=data['phone'],
        email=data.get('email', ''),
        address=data.get('address', '')
    )
    db.session.add(new_owner)
    db.session.commit()
    return new_owner

def get_all_owners():
    return Owner.query.all()

def get_owner_by_id(owner_id):
    return Owner.query.get(owner_id)
