from flask import Blueprint, render_template, request
from models.property_model import Property
from models.requirement_model import UserRequirement

from database.db import db
from sqlalchemy import text

main_bp = Blueprint('main', __name__)

@main_bp.route('/fix-database')
def fix_database():
    try:
        # Using raw SQL to add columns if they don't exist
        with db.engine.connect() as conn:
            # Add user_id to properties
            try:
                conn.execute(text("ALTER TABLE properties ADD COLUMN user_id INTEGER REFERENCES users(id)"))
                conn.commit()
            except Exception: pass
            
            # Add is_public to properties
            try:
                conn.execute(text("ALTER TABLE properties ADD COLUMN is_public BOOLEAN DEFAULT 1"))
                conn.commit()
            except Exception: pass
            
            # Add role to users
            try:
                conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'Buyer'"))
                conn.commit()
            except Exception: pass
            
        return "Database updated successfully! You can now go back to the <a href='/'>Home Page</a> and the error should be gone."
    except Exception as e:
        return f"Error updating database: {str(e)}"

@main_bp.route('/')
def index():
    # Show featured properties on homepage
    featured_properties = Property.query.filter_by(is_featured=True).limit(6).all()
    if not featured_properties:
        featured_properties = Property.query.limit(6).all()
    return render_template('home.html', properties=featured_properties)

@main_bp.route('/search')
def search():
    query = Property.query
    location = request.args.get('location', 'Nashik')
    listing_type = request.args.get('listing_type')
    bhk = request.args.get('bhk')
    
    if location:
        query = query.filter(Property.location.ilike(f'%{location}%'))
    if listing_type:
        query = query.filter_by(listing_type=listing_type)
    if bhk:
        query = query.filter_by(bhk=int(bhk))
        
    properties = query.all()
    return render_template('search.html', properties=properties)

@main_bp.route('/property/<int:id>')
def property_detail(id):
    property = Property.query.get_or_404(id)
    return render_template('property_detail.html', property=property)

@main_bp.route('/customer-needs')
def customer_needs():
    # Show Pending or Contacted requirements on the public page
    needs = UserRequirement.query.filter(UserRequirement.status.in_(['Pending', 'Contacted'])).order_by(UserRequirement.created_at.desc()).all()
    return render_template('customer_needs.html', needs=needs)
