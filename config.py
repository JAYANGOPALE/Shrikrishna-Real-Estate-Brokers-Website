import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_super_secret_key_change_in_production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///shrikrishna_real_estate.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt_secret_key_change_in_production')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', 'property_images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
