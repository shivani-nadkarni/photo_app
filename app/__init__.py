from flask import Flask

app = Flask(__name__)

from app import routes

#database initialisation
# from . import db
# db.init_app(app)


