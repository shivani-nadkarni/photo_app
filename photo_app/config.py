"""Creates Config objec with variables to be used throughout the application"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = '1234sasdf//;;'
    DATABASE = 'photo_app.db'
    UPLOAD_FOLDER = 'upload_folder'
    ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'photo_app.db')
