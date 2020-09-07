from app import app
from flask import render_template, request, g, session
import sqlite3

#database path
DATABASE = '/home/shivani/Learning/python/photo_app/photo_app'

#establish database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
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
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#initialising schema
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# some other useful functions
# def convert_image_to_blob(file):
#   Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         blobData = file.read()
#     return blobData



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

    if user and password == user['password']:
        session['username'] = username
        session['user_id'] = user['id']
        return render_template("my_photos.html", session=session)
    else:
        print("login failed")
        return render_template("login.html", message='Incorrect username/password. Try again!')

"""
@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('my_photos.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('my_photos.html', session=session, message='Error occurred. Retry uploading')
        if file:
            # blob_data = convert_image_to_blob(file)
            blob_data = file
            user_id = session.user.id
            result = query_db('INSERT INTO photos (user_id, photo) VALUES (?, ?)', [user_id, blob_data], one=True)
            return redirect('my_photos.html', message='file uploaded successfully')
    return redirect('my_photos.html', session=session)
"""

@app.route("/logout")
def logout():
    return index()
