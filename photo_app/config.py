"""Creates Config object with variables to be used throughout the application"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    S3_URL = os.environ.get('S3_URL')
    S3_KEY = os.environ.get('S3_KEY')
    S3_SECRET = os.environ.get('S3_SECRET')
    S3_BUCKET = os.environ.get('S3_BUCKET')
    S3_LOCATION = '{}/{}/'.format(S3_URL, S3_BUCKET)
