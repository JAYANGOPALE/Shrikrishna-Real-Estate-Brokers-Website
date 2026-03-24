import os
import urllib.parse

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_super_secret_key_change_in_production')
    
    # Safely handle special characters in DATABASE_URL passwords
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///shrikrishna_real_estate.db')
    if db_url.startswith("postgresql://") and ":" in db_url and "@" in db_url:
        try:
            # Format: postgresql://user:password@host:port/dbname
            prefix, rest = db_url.split("://", 1)
            user_pass, host_db = rest.rsplit("@", 1)
            if ":" in user_pass:
                user, password = user_pass.split(":", 1)
                encoded_password = urllib.parse.quote_plus(password)
                db_url = f"{prefix}://{user}:{encoded_password}@{host_db}"
        except Exception as e:
            print(f"Warning: Could not auto-encode DB password: {e}")
            
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt_secret_key_change_in_production')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', 'property_images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
