"""Creates Config object with variables to be used throughout the application"""

import os

class Config():
    """This class contains all config variables to be used in the application.
    Few values are set here, some are obtained from the environment.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY')
    ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # These values are used for S3(object storage) connection
    S3_URL = os.environ.get('S3_URL')
    S3_KEY = os.environ.get('S3_KEY')
    S3_SECRET = os.environ.get('S3_SECRET')
    S3_BUCKET = os.environ.get('S3_BUCKET')
    S3_LOCATION = '{}/{}/'.format(S3_URL, S3_BUCKET)
