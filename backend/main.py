import json
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
async_mode = None

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('connect')
def test_connect():
    socketio.emit('my response', {'data': 'Connected\n', 'count': 0})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@app.route('/card_info', methods=['POST'])
def send_card_info_socket():
    record = json.loads(request.data)
    print(record)
    socketio.emit('update_card', record)
    return jsonify(record)

if __name__ == '__main__':
    socketio.run(app)