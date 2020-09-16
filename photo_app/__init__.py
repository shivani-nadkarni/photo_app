"""This module initialises and configures flask object"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from photo_app.config import Config

app = Flask(__name__)

app.config.from_object(Config)
