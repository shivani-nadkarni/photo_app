"""This module starts the flask server."""

from photo_app.routes import app

# Start the flask server
if __name__ == '__main__':
    app.run()
