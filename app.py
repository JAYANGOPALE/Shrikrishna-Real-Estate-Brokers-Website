import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from config import Config
from database.db import db

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    Migrate(app, db)
    CORS(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models.user_model import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.main import main_bp
    from routes.requirement_routes import requirement_bp
    from routes.property_routes import property_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(requirement_bp, url_prefix='/requirements')
    app.register_blueprint(property_bp, url_prefix='/property')

    # Auto-fix database schema on startup
    with app.app_context():
        from sqlalchemy import text
        try:
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
        except Exception as e:
            print(f"Migration error: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
