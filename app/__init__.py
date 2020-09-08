from flask import Flask
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

from app import routes

#database initialisation
# from . import db
# db.init_app(app)


