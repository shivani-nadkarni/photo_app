from app import app
from flask import render_template, request


@app.route('/')
@app.route('/index')
def index():
	return render_template('login.html', title='Login')

@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	return render_template("my_photos.html", username=username)