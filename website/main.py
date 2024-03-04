from flask import session
from flask_socketio import SocketIO
import time
from application import create_app
from application.database import DataBase
import config

app = create_app() # Create a working application through __init__.py method
socketio = SocketIO(app)  # Create a socket that handles connections from multiple users

@socketio.on('event')
def chatmeleon(json, methods=['GET', 'POST']): # Handles all messages being sent to the web server by users
    data = dict(json)
    if "name" in data: # If event contains a "name"
        db = DataBase()
        db.save_message(data["name"], data["message"])

    socketio.emit('message response', json)

if __name__ == "__main__":  # Start web server using the socket
    socketio.run(app, debug=True, host=str(config.Config.SERVER))
