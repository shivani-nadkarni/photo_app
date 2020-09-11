DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS photos;

CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE photos (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	photo_path TEXT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users (id)
);

INSERT INTO users (username, password) 
VALUES ('Shivani', '123');

INSERT INTO users (username, password) 
VALUES ('Viren', '456');