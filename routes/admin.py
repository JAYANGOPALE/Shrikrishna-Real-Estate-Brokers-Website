import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.property_model import Property
from models.property_images_model import PropertyImage
from models.requirement_model import UserRequirement
from models.owner_model import Owner
from database.db import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@admin_bp.before_request
@login_required
def ensure_admin():
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
def dashboard():
    properties = Property.query.filter_by(is_public=True).order_by(Property.created_at.desc()).all()
    hidden_properties = Property.query.filter_by(is_public=False).order_by(Property.created_at.desc()).all()
    requirements = UserRequirement.query.order_by(UserRequirement.created_at.desc()).all()
    
    # Matching Logic
    matches = []
    for req in requirements:
        # Match based on Location, BHK, and Price within budget range
        matched_props = Property.query.filter(
            Property.location.ilike(f"%{req.location}%"),
            Property.bhk == int(req.bhk.replace('BHK', '').strip()) if 'BHK' in req.bhk else Property.bhk == req.bhk,
            Property.price >= req.budget_min,
            Property.price <= req.budget_max
        ).all()
        
        for p in matched_props:
            matches.append({
                'buyer': req,
                'property': p
            })
            
    return render_template('admin/dashboard.html', 
                           properties=properties, 
                           hidden_properties=hidden_properties, 
                           requirements=requirements,
                           matches=matches)

@admin_bp.route('/property/approve/<int:id>', methods=['POST'])
def approve_property(id):
    prop = Property.query.get_or_404(id)
    prop.is_public = True
    db.session.commit()
    flash('Property approved and moved to public listings.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/property/add', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location', 'Nashik')
        price = float(request.form.get('price'))
        bhk = int(request.form.get('bhk'))
        area = float(request.form.get('area'))
        listing_type = request.form.get('listing_type') # Rent/Sale
        property_type = request.form.get('property_type')
        description = request.form.get('description')
        is_featured = True if request.form.get('is_featured') else False

        new_prop = Property(
            title=title, location=location, price=price, bhk=bhk,
            area=area, listing_type=listing_type, property_type=property_type,
            description=description, is_featured=is_featured
        )
        db.session.add(new_prop)
        db.session.flush() # To get property_id

        # Handle Multiple Images
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{new_prop.property_id}_{datetime.now().timestamp()}_{file.filename}")
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'property_images', filename)
                file.save(upload_path)
                
                img = PropertyImage(property_id=new_prop.property_id, image_path=filename)
                db.session.add(img)

        db.session.commit()
        flash('Property added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/property_form.html', action="Add")

@admin_bp.route('/property/edit/<int:id>', methods=['GET', 'POST'])
def edit_property(id):
    prop = Property.query.get_or_404(id)
    if request.method == 'POST':
        prop.title = request.form.get('title')
        prop.price = float(request.form.get('price'))
        prop.bhk = int(request.form.get('bhk'))
        prop.area = float(request.form.get('area'))
        prop.listing_type = request.form.get('listing_type')
        prop.property_type = request.form.get('property_type')
        prop.description = request.form.get('description')
        prop.is_featured = True if request.form.get('is_featured') else False

        # Handle Multiple Images on Edit
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{prop.property_id}_{datetime.now().timestamp()}_{file.filename}")
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'property_images', filename)
                file.save(upload_path)
                
                img = PropertyImage(property_id=prop.property_id, image_path=filename)
                db.session.add(img)

        db.session.commit()
        flash('Property updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/property_form.html', prop=prop, action="Edit")

@admin_bp.route('/property/delete/<int:id>', methods=['POST'])
def delete_property(id):
    prop = Property.query.get_or_404(id)
    db.session.delete(prop)
    db.session.commit()
    flash('Property deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/requirement/add', methods=['GET', 'POST'])
def add_requirement():
    if request.method == 'POST':
        # Map old form to new model as best as possible
        title = request.form.get('title')
        budget = request.form.get('budget')
        location = request.form.get('location', 'Nashik')
        description = request.form.get('description')

        # Since new model needs more fields and user_id, 
        # we'll use current_user.id and defaults for other fields
        new_req = UserRequirement(
            user_id=current_user.id,
            requirement_type='Buy', # Default
            property_type='Flat', # Default
            location=location,
            budget_min=0, # Default
            budget_max=1000000, # Default (or parse from budget if numeric)
            description=f"{title}: {description}",
            contact_preference='Both'
        )
        db.session.add(new_req)
        db.session.commit()
        flash('Customer requirement posted successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/requirement_form.html', action="Add")

@admin_bp.route('/requirement/delete/<int:id>', methods=['POST'])
def delete_requirement(id):
    req = UserRequirement.query.get_or_404(id)
    db.session.delete(req)
    db.session.commit()
    flash('Requirement deleted.', 'success')
    return redirect(url_for('admin.dashboard'))
