from models.property_model import Property
from models.property_images_model import PropertyImage
from models.owner_model import Owner
from database.db import db
from utils.image_upload import save_image

def create_property(data, files):
    try:
        new_property = Property(
            title=data['title'],
            location=data['location'],
            price=float(data['price']),
            bhk=int(data['bhk']),
            area=float(data['area']),
            property_type=data['property_type'],
            description=data.get('description', ''),
            owner_id=int(data['owner_id'])
        )
        db.session.add(new_property)
        db.session.flush() # Get ID

        if 'images' in files:
            images = files.getlist('images')
            for img in images:
                path = save_image(img)
                if path:
                    new_image = PropertyImage(property_id=new_property.property_id, image_path=path)
                    db.session.add(new_image)
        
        db.session.commit()
        return new_property
    except Exception as e:
        db.session.rollback()
        raise e

def get_all_properties():
    return Property.query.all()

def get_property_by_id(property_id):
    return Property.query.get(property_id)

def update_property(property_id, data):
    prop = Property.query.get(property_id)
    if not prop:
        return None
    
    if 'title' in data: prop.title = data['title']
    if 'location' in data: prop.location = data['location']
    if 'price' in data: prop.price = float(data['price'])
    if 'bhk' in data: prop.bhk = int(data['bhk'])
    if 'area' in data: prop.area = float(data['area'])
    if 'property_type' in data: prop.property_type = data['property_type']
    if 'description' in data: prop.description = data['description']
    
    db.session.commit()
    return prop

def delete_property(property_id):
    prop = Property.query.get(property_id)
    if prop:
        db.session.delete(prop)
        db.session.commit()
        return True
    return False
