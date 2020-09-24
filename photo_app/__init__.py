"""This module initialises and configures the flask object."""

from flask import Flask
from photo_app.config import Config

# Flask object
app = Flask(__name__)

# Configuration of flask object
app.config.from_object(Config)
