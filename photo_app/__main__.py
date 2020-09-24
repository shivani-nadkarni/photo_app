"""this module starts flask server"""
from photo_app.routes import app
# from photo_app.helpers import *
print(__name__)
if __name__ == '__main__':
    app.run()


# f = open("config.py", "r")
# upload_file_to_s3('shivani', f, 'mytestbucket')
