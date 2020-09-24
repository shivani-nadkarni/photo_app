"""Definitions for routes."""
from flask import render_template, request, session, redirect
from werkzeug.utils import secure_filename
from photo_app import app
from photo_app.db import database, User, Photo
from photo_app.helpers import upload_file_to_s3

# Checks if filename has an image extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in\
    app.config['ALLOWED_EXTENSIONS']

# Endpoint for login page.
@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html', title='Login')

# Endpoint for /home.
# The second endpoint is used when values are passed from my 'my_photos.html'.
@app.route('/home')
@app.route('/home/<message>/<success>', methods=['GET'])
def home(session, message, success):
    if session['logged_in']:
        photos = Photo.query.filter_by(user_id=session['user_id']).all()
        return render_template("my_photos.html", session=session,
                               photos=photos, message=message,
                               success=success, s3_location=app.config['S3_LOCATION'])
    return index()

# endpoint for /login
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        #fetch user input
        username = request.form['username']
        password = request.form['password']

        #query to fetch user record if exists
        user = User.query.filter_by(username=username).first()

        #Validation
        if user and password == user.password:
            session['username'] = username
            session['user_id'] = user.user_id
            session['logged_in'] = True
            return home(session=session, message=False, success=False)
        return render_template("login.html",
                                   message="Incorrect username/password. Retry again.")

    elif session['logged_in'] and request.method == 'GET':
        return home(session=session, message=False, success=False)

    return redirect('/index')

# Executed when this endpoint is requested or when upload button is clicked.
@app.route("/upload", methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return home(session=session, message='No file selected. Retry uploading.',
                        success=False)

        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file_path = '{}/{}'.format(session['username'], file_name)

            # upload to minio
            upload_file_to_s3(file_path, file, app.config['S3_BUCKET'])

            #save filename into the database
            photo = Photo(file_path=file_path)
            user = User.query.filter_by(user_id=session['user_id']).first()
            user.photos.append(photo)
            database.session.commit()
            return home(session=session, message='File uploaded successfully.', success=True)

    elif request.method == 'GET' and session['logged_in']:
        return home(session=session, message=False, success=False)

    return redirect('/index')

# Executed when the user logs out.
@app.route("/logout")
def logout():
    if session['logged_in']:
        session['logged_in'] = False
    return redirect('/index')
