from flask import Flask
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from app import routes

#database initialisation
# from . import db
# db.init_app(app)


