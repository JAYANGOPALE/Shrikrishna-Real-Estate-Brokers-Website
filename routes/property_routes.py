import os
from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.property_model import Property
from models.property_images_model import PropertyImage
from database.db import db
from services.property_service import get_all_properties, get_property_by_id
from services.search_service import search_properties
from utils.response_format import success_response, error_response
from ml_model.price_prediction_model import predictor
from ml_model.recommendation_model import recommender

property_bp = Blueprint('property', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@property_bp.route('/post', methods=['GET', 'POST'])
@login_required
def post_property():
    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location', 'Nashik')
        price = float(request.form.get('price'))
        bhk = int(request.form.get('bhk'))
        area = float(request.form.get('area'))
        listing_type = request.form.get('listing_type')
        property_type = request.form.get('property_type')
        description = request.form.get('description')

        new_prop = Property(
            title=title, location=location, price=price, bhk=bhk,
            area=area, listing_type=listing_type, property_type=property_type,
            description=description, 
            user_id=current_user.id,
            is_public=False # Hidden by default for Admin approval
        )
        db.session.add(new_prop)
        db.session.flush()

        # Handle Multiple Images
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(f"user_{current_user.id}_{datetime.now().timestamp()}_{file.filename}")
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'property_images', filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                file.save(upload_path)
                
                img = PropertyImage(property_id=new_prop.property_id, image_path=filename)
                db.session.add(img)

        db.session.commit()
        flash('Property submitted successfully! It will be visible after admin approval.', 'success')
        return redirect(url_for('main.index'))

    return render_template('post_property.html')

@property_bp.route('/', methods=['GET'])
def get_properties():
    filters = request.args
    if filters:
        properties = search_properties(filters)
    else:
        properties = get_all_properties()
    
    result = []
    for p in properties:
        result.append({
            'property_id': p.property_id,
            'title': p.title,
            'location': p.location,
            'price': p.price,
            'bhk': p.bhk,
            'area': p.area,
            'property_type': p.property_type,
            'description': p.description,
            'images': [img.image_path for img in p.images]
        })
    
    return success_response(data=result)

@property_bp.route('/<int:property_id>', methods=['GET'])
def get_property(property_id):
    p = get_property_by_id(property_id)
    if not p:
        return error_response("Property not found", 404)
    
    data = {
        'property_id': p.property_id,
        'title': p.title,
        'location': p.location,
        'price': p.price,
        'bhk': p.bhk,
        'area': p.area,
        'property_type': p.property_type,
        'description': p.description,
        'images': [img.image_path for img in p.images]
    }
    return success_response(data=data)

@property_bp.route('/predict_price', methods=['POST'])
def predict_price():
    data = request.get_json()
    # location, bhk, area, property_type
    try:
        price = predictor.predict(
            data['location'], 
            int(data['bhk']), 
            float(data['area']), 
            data['property_type']
        )
        return success_response(data={'estimated_price': price})
    except Exception as e:
        return error_response(str(e), 500)

@property_bp.route('/<int:property_id>/recommendations', methods=['GET'])
def get_recommendations(property_id):
    all_props = get_all_properties()
    # Serialize for recommender
    props_data = []
    for p in all_props:
        props_data.append({
            'property_id': p.property_id,
            'location': p.location,
            'property_type': p.property_type,
            'description': p.description,
            'title': p.title, # Needed for return?
            'price': p.price,
            'images': [img.image_path for img in p.images]
        })
    
    recs = recommender.recommend(property_id, props_data)
    
    return success_response(data=recs)
