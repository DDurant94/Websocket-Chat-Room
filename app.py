from web_socket_server import WebSocketServer, socketio, app
from flask import render_template

app = WebSocketServer().create_app()
message_storage = {}
  
@socketio.on('message')
def handle_message(data):
  user = data['user']
  message = data['message']
  print(f'Received message from {user}: {message}')
  
  if user not in message_storage:
    message_storage[user] = []
  message_storage[user].append(message)
    
  socketio.emit('message', data)
  
@socketio.on('get_user_messages')
def handle_get_user_messages(data):
  user = data['user']
  user_messages = message_storage.get(user, [])
  socketio.emit('get_user_messages', {'user': user, 'messages': user_messages})
  
@socketio.on('connect')
def handle_connect():
  print('Client connected')
  
@socketio.on('disconnect')
def handle_disconnect():
  print('Client disconnected')
  
@app.route('/')
def index():
  return render_template('WebSocketClient.html')
  
if __name__ == '__main__':
  socketio.run(app)