"""Defines user, photo classes.
   Creates database 'photo_app'.
   Enters some data in 'users' table"""

from flask_sqlalchemy import SQLAlchemy
from photo_app.routes import app

# Database object is created and associated to the main application object here.
database = SQLAlchemy(app)

# User class specifies the attributes and characteristics for table 'users'
class User(database.Model):
    __tablename__ = 'users'
    user_id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(20), nullable=False)
    password = database.Column(database.String(20), nullable=False)
    photos = database.relationship('Photo', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

# This class specifies the attributes and characteristics for table 'photo'
class Photo(database.Model):
    __tablename__ = 'photo'
    photo_id = database.Column(database.Integer, primary_key = True)
    filename = database.Column(database.String(50), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return '<Photo {}>'.format(self.filename)

"""The function creates database 'photo_app' and the tables(users, photo) in it. 
    Enters some user data in 'users' table."""
def create_db():
    database.create_all()

    admin = User(username='admin', password='admin')
    guest = User(username='guest', password='guest')

    database.session.add(admin)
    database.session.add(guest)
    database.session.commit()
