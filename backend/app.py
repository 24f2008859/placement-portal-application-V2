from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail 
from flask_caching import Cache
from config import Config 



mail = Mail()
db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mail.init_app(app)

    cache.init_app(app) 

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from auth import auth_bp
    app.register_blueprint(auth_bp)

    from admin import admin_bp
    app.register_blueprint(admin_bp)

    from company import company_bp
    app.register_blueprint(company_bp)

    from student import student_bp 
    app.register_blueprint(student_bp)

    from public import public_bp
    app.register_blueprint(public_bp)

    return app