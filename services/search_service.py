from models.property_model import Property

def search_properties(filters):
    query = Property.query

    if 'location' in filters and filters['location']:
        query = query.filter(Property.location.ilike(f"%{filters['location']}%"))
    
    if 'min_price' in filters and filters['min_price']:
        query = query.filter(Property.price >= float(filters['min_price']))
    
    if 'max_price' in filters and filters['max_price']:
        query = query.filter(Property.price <= float(filters['max_price']))
    
    if 'bhk' in filters and filters['bhk']:
        query = query.filter(Property.bhk == int(filters['bhk']))
        
    if 'property_type' in filters and filters['property_type']:
        query = query.filter(Property.property_type.ilike(f"%{filters['property_type']}%"))
        
    if 'min_area' in filters and filters['min_area']:
        query = query.filter(Property.area >= float(filters['min_area']))

    return query.all()
