import os 
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///placeme.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'resume')
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None 
    MAIL_PASSWORD = None 
    MAIL_DEFAULT_SENDER = 'placeme@example.com'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://localhost:6379/1'
    CACHE_DEFAULT_TIMEOUT = 300