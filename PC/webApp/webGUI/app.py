from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, session, request, send_from_directory
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, \
	close_room, disconnect
import serial

s = serial.Serial('/dev/ttyACM0', 115200, timeout=0.2)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/assets/<path:filename>')
def send_foo(filename):
	print(filename)
	return send_from_directory('static/assets', filename)
	return app


@socketio.on('arduino', namespace='/test')
def arduino_message(message):
	
	session['receive_count'] = session.get('receive_count', 0) + 1
	msg = message['data']
	
	print(type(msg));
	msg = msg.encode('ascii');
	print(type(msg));
	s.write(msg+'\n\r')
	#test = s.readline();
	
	#response = "Message '" + test + "' received from arduino"
	#print(response)
	
	response = "Message '" + msg + "' sent to arduino"
	print(response)
	emit('my response', {'data': response, 'count': session['receive_count']})


if __name__ == '__main__':
	socketio.run(app)
