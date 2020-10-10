"""Definitions for routes."""

from flask import render_template, request, session, redirect
from werkzeug.utils import secure_filename
from photo_app import app, database
from photo_app.models import User, Photo
from photo_app.helpers import upload_file_to_s3, create_presigned_url

def allowed_file(filename):
    """Checks if the file has an image extension.

    :param filename: name of the file with the extension
    """

    return '.' in filename and filename.rsplit('.', 1)[1].lower()\
                               in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
@app.route('/index')
def index():
    """Displays the login page."""

    return render_template('login.html', title='Login')

@app.route('/home')
@app.route('/home/<message>/<success>', methods=['GET'])
def home(session, message, success):
    """Endpoint for /home.
    The second endpoint is used when values are passed from my 'my_photos.html'.

    :param session: contains session variables username, user_id and logged_in
    :param message: contains message whether file upload is successful or not
    :param success: boolean value, true if successful upload else false
    """

    if session['logged_in']:
        photos = Photo.query.filter_by(user_id=session['user_id']).all()

        bucket_name = app.config['S3_BUCKET']
        url_list = []

        # fetches urls of all S3 pictures
        for photo in photos:
            url = create_presigned_url(bucket_name, photo.file_path)
            url_list.append(url)

        return render_template("my_photos.html",
                               session=session,
                               photos=url_list,
                               message=message,
                               success=success,
                               s3_location=app.config['S3_LOCATION'])
    return index()

# endpoint for /login
@app.route('/login', methods=['POST','GET'])
def login():
    """Fetches the user input 'username' and password.
    Performs validation of password against username.

    If true, go to the user's home page else give and alert message as
    'Incorrect username/password'. Prompt the user to renter the credentials.
    """

    if request.method == 'POST':
        #fetch user input
        username = request.form['username']
        password = request.form['password']

        #query to fetch user record if exists
        user = User.query.filter_by(username=username).first()

        # Validation successful
        if user and password == user.password:
            # Setting session values
            session['username'] = username
            session['user_id'] = user.user_id
            session['logged_in'] = True

            # Redirect to user home page
            return home(session=session,
                        message=False,
                        success=False)

        # Validation failed
        return render_template(
                "login.html",
                message="Incorrect username/password. Retry again.")

    # When the user is logged-in and the endpoint is requested
    elif session['logged_in'] and request.method == 'GET':
        return home(session=session,
                    message=False,
                    success=False)

    # When the user is not logged-in and the endpoint is requested
    return redirect('/index')

@app.route("/upload", methods=['POST','GET'])
def upload():
    """Executed when the upload button is clicked or upload endpoint is
    requested.

    If file is selected, then give success message else alert the user that file
    is not selected.
    """

    # If user clicks upload button
    if request.method == 'POST':
        # Fetch the file
        file = request.files['file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return home(session=session,
                        message='No file selected. Retry uploading.',
                        success=False)

        # If file is selected and has an image extension
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)

            # Create file path for image storage in S3, relative to bucket
            file_path = '{}/{}'.format(session['username'], file_name)

            # Upload to s3
            upload_file_to_s3(file_path, file, app.config['S3_BUCKET'])

            # New Photo object98juug
            photo = Photo(file_path=file_path)

            # Obtain User object for the logged in user
            user = User.query.filter_by(user_id=session['user_id']).first()

            # Adding the Photo object
            user.photos.append(photo)

            # Commit the additions
            database.session.commit()
            return home(session=session,
                        message='File uploaded successfully.',
                        success=True)

    # When the user is logged-in and the endpoint is requested
    elif request.method == 'GET' and session['logged_in']:
        return home(session=session,
                    message=False,
                    success=False)

    # When the user is not logged-in and the endpoint is requested
    return redirect('/index')

@app.route("/logout")
def logout():
    """Executed when the user logs out."""

    if session['logged_in']:
        session['logged_in'] = False
    return redirect('/index')
