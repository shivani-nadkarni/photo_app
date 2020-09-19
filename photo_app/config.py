"""Creates Config objec with variables to be used throughout the application"""
import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = 'upload_folder'
    ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
