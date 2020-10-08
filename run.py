import os
from photo_app import app
from photo_app import routes

if __name__ == '__main__':
	# Start the flask server
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
