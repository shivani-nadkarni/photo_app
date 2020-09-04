from flask_login import LoginManager
from app import app

login_manager = LoginManager()
login_manager.init_app(app)