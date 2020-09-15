"""Defines user, photo class, creates database, enters some data"""
from flask_sqlalchemy import SQLAlchemy
from photo_app.routes import app

database = SQLAlchemy(app)

class User(database.Model):
    __tablename__ = 'user'
    user_id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(20), nullable=False)
    password = database.Column(database.String(20), nullable=False)  
    photos = database.relationship('Photo', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Photo(database.Model):
    __tablename__ = 'photo'
    photo_id = database.Column(database.Integer, primary_key = True)
    filename = database.Column(database.String(50), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return '<Photo {}>'.format(self.filename, self.user_id)

def create_db():
    database.create_all()

    admin = User(username='admin', password='admin')
    guest = User(username='guest', password='guest')

    database.session.add(admin)
    database.session.add(guest)
    database.session.commit()
