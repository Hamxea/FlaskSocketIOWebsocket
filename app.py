import sqlite3
from flask import Flask, render_template, url_for, redirect, request
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


clients = []


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    clients.append(request.sid)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected....')
    clients.remove(request.sid)


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    #send(msg, broadcast=True)
    socketio.emit('message', 'Change has been made (from server): ' + msg, broadcast=True)


def send_message(client_id, data):
    socketio.emit('output', data, room=client_id)
    print('sending message "{}" to client "{}".'.format(data, client_id))


@app.route('/ping')
def ping():
    socketio.emit('ping event', {'data': 42}, namespace='/chat')

if __name__ == '__main__':
    #app.run()
    socketio.run(app)