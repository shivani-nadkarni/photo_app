"""Defines 'User', 'Photo' classes.
Creates database 'photo_app'.
Enters some records in 'users' table.
"""

from photo_app import database

# # Create database object and associate it to the main application object
# database = SQLAlchemy(app)

class User(database.Model):
    """ User class specifies the attributes and characteristics for table
    'users'.
    """

    # Set tablename as 'users'
    __tablename__ = 'users'

    # Define attributes
    user_id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(20), nullable=False)
    password = database.Column(database.String(20), nullable=False)
    photos = database.relationship('Photo', backref='author', lazy='dynamic')

    def __repr__(self):
        """Specifies how the table records will be printed on the console"""

        return '<User {}>'.format(self.username)

class Photo(database.Model):
    """This class specifies the attributes and characteristics for table 'photo'
    """

    # Set tablename as 'photo'
    __tablename__ = 'photo'

    # Define attributes
    photo_id = database.Column(database.Integer, primary_key = True)
    file_path = database.Column(database.String(50), nullable=False)
    user_id = database.Column(database.Integer,
                              database.ForeignKey('users.user_id'),
                              nullable=False)

    def __repr__(self):
        """Specifies how the table records will be printed on the console"""

        return '<Photo {}>'.format(self.filename)

def create_db():
    """This function creates database 'photo_app' with the tables 'users' and
    'photo'.
    Also, adds two records in 'users' table.
    """

    # Database creation
    database.create_all()

    # Create two User objects
    admin = User(username='admin', password='admin')
    guest = User(username='guest', password='guest')

    # Add objects to the database
    database.session.add(admin)
    database.session.add(guest)

    # Commit the changes
    database.session.commit()
