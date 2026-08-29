# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration — all secrets from environment variables
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-insecure-key")
    
    db_url = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    
    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from routes import main
    app.register_blueprint(main)
    
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)