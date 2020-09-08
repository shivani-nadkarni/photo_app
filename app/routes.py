from app import app
from flask import render_template, request, g, session, flash, redirect
import sqlite3
from werkzeug.utils import secure_filename
import os
import pathlib

#database path
# DATABASE = '/home/shivani/Learning/python/photo_app/photo_app'

#establish database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

#close database connetion
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#execute queries
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    print(cur.lastrowid)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#perform insertion
def insert_photo(query, args=()):
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    return cur.lastrowid

#initialising schema
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#routes
@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html', title='Login')

@app.route('/login', methods=['POST'])
def login():
    #fetch user input
    username = request.form['username']
    password = request.form['password']

    #query to fetch user record if exists
    user = query_db('select * from users where username = ?',
                [username], one=True)

    #Validation
    if user and password == user['password']:
        session['username'] = username
        session['user_id'] = user['id']
        return render_template("my_photos.html", session=session)
    else:
        print("login failed")
        return render_template("login.html", message='Incorrect username/password. Try again!')


@app.route("/upload", methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return render_template('my_photos.html', session=session, failure='No file selected. Retry uploading.')
        if file:
            filename = secure_filename(file.filename)
            photo_path = app.config['UPLOAD_FOLDER'] + '/' + session['username']  
            
            #creates new folder for each user only for the first uplaod
            pathlib.Path(app.config['UPLOAD_FOLDER'], session['username']).mkdir(exist_ok=True)
            
            file.save(os.path.join(photo_path, filename))
            result = insert_photo('INSERT INTO photos (user_id, photo_path) VALUES (?,?)', [session['user_id'], photo_path])
            return render_template('my_photos.html', session=session, success='File uploaded successfully.')
    return render_template('my_photos.html')


@app.route("/logout")
def logout():
    return index()
