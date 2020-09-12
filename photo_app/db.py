import sqlite3
from flask import g

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

