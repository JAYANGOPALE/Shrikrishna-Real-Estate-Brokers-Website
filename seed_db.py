import os
import csv
from app import create_app
from database.db import db
from models.user_model import User
from models.owner_model import Owner
from models.property_model import Property
from models.property_images_model import PropertyImage
from models.requirement_model import UserRequirement
from models.inquiry_model import Inquiry

def seed_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()

        # 1. Create Admin User
        admin_email = 'shrikrishnabrokers18@gmail.com'
        admin_pass = '@_pass_123'
        
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(name='Admin', email=admin_email, phone='1234567890', is_admin=True)
            admin.set_password(admin_pass)
            db.session.add(admin)
            print(f"Admin user {admin_email} created.")
        else:
            admin.set_password(admin_pass)
            admin.is_admin = True
            print(f"Admin user {admin_email} password updated.")

        # 2. Create Regular User
        user = User.query.filter_by(email='user@example.com').first()
        if not user:
            user = User(name='John Doe', email='user@example.com', phone='9876543210', is_admin=False)
            user.set_password('user123')
            db.session.add(user)
            print("Regular user created.")
        
        db.session.commit() # Commit to get user.id

        # 3. Create an Owner
        if not Owner.query.filter_by(owner_name='Ram Krishna').first():
            owner = Owner(owner_name='Ram Krishna', phone='9988776655', email='ram@example.com', address='Mumbai, Maharashtra')
            db.session.add(owner)
            db.session.flush() # Get owner_id
            print("Owner created.")
        else:
            owner = Owner.query.filter_by(owner_name='Ram Krishna').first()

        # 4. Create User Requirements
        if not UserRequirement.query.first():
            reqs = [
                UserRequirement(user_id=user.id, requirement_type='Buy', property_type='Flat', location='Nashik', budget_min=3000000, budget_max=5000000, bhk='2BHK', description='Looking for a 2BHK flat in Nashik city area.', contact_preference='Call'),
                UserRequirement(user_id=user.id, requirement_type='Rent', property_type='Commercial', location='College Road, Nashik', budget_min=20000, budget_max=30000, description='Need a small shop for boutique.', contact_preference='Both')
            ]
            db.session.add_all(reqs)
            print("User requirements seeded.")

        # 5. Load Properties from CSV
        csv_path = os.path.join('ml_model', 'dataset', 'dummy_data.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = f"{row['bhk']} BHK {row['property_type']} in {row['location']}"
                    # Check if property already exists
                    existing = Property.query.filter_by(title=title).first()
                    if not existing:
                        new_prop = Property(
                            title=title,
                            location=row['location'],
                            price=float(row['price']),
                            bhk=int(row['bhk']),
                            area=float(row['area']),
                            listing_type='Sale',
                            property_type=row['property_type'],
                            description=f"A beautiful {row['bhk']} BHK {row['property_type']} located in {row['location']}. Features {row['area']} sqft of living space.",
                            owner_id=owner.owner_id,
                            is_featured=True
                        )
                        db.session.add(new_prop)
            print(f"Properties seeded from {csv_path}.")
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
