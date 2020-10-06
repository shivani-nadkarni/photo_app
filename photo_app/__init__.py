"""This module initialises and configures the flask object."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Flask object
app = Flask(__name__)

# Configuration of flask object
app.config.from_object(Config)

# Define the database object which is imported
# by modules and controllers
database = SQLAlchemy(app)
