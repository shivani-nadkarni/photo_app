"""Definitions for routes and database operations"""
import os
import pathlib
from flask import render_template, request, g, session, redirect, send_from_directory
from werkzeug.utils import secure_filename
from photo_app import app
from photo_app.db import database, User, Photo

# Checks if filename has image extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in\
    app.config['ALLOWED_EXTENSIONS']

# routes
@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html', title='Login')

# endpoint for /login
@app.route('/home')
@app.route('/home/<message>/<success>', methods=['GET'])
def home(session, message, success):
    if session['logged_in']:
        photos = Photo.query.filter_by(user_id=session['user_id']).all()
        return render_template("my_photos.html", session=session,
                               photos=photos, message=message,
                               success=success)
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
        else:
            return render_template("login.html", message="Incorrect username/password. Retry again.")

    elif session['logged_in'] and request.method == 'GET':
        return home(session=session, message=False, success=False)

    return redirect('/index')

# Executed when this endpoint is requested or when upload is clicked
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

        if file:
            filename = secure_filename(file.filename)

            #creates new folder for each user only for the first uplaod
            pathlib.Path(app.config['UPLOAD_FOLDER'], session['username']).mkdir(exist_ok=True)

            #saving the file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], session['username'], filename))

            #save filename into the database
            photo = Photo(filename=filename)
            user = User.query.filter_by(user_id=session['user_id']).first()
            user.photos.append(photo)
            database.session.commit()
            return home(session=session, message='File uploaded successfully.', success=True)

    elif request.method == 'GET' and session['logged_in']:
        return home(session=session, message=False, success=False)

    return redirect('/index')

# This is executed when image link is clicked on home page
@app.route("/images/<filename>")
def get_image(filename):
    if session['logged_in']:
        return send_from_directory(os.path.join('..',
                                   app.config['UPLOAD_FOLDER'],
                                   session['username']), filename)
    return redirect('/index')

# Executed when user logs out
@app.route("/logout")
def logout():
    if session['logged_in']:
        session['logged_in'] = False
    return redirect('/index')
