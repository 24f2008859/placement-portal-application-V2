import os 
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///placeme.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'resume')
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}