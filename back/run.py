from flask import Flask, render_template, request, jsonify
from subprocess import call
from flask_socketio import SocketIO, send
from http import HTTPStatus


app = Flask(__name__)
socket_io = SocketIO(app)

@app.route('/')
def hello_world():
    return "Hello Gaemigo Project Home Page!!"

@app.route('/chat')
def chatting():
    return render_template('chat.html')

@socket_io.on("message")
def request(message):
    print("message : "+ message)
    to_client = dict()
    if message == 'new_connect':
        to_client['message'] = "새로운 유저가 난입하였다!!"
        to_client['type'] = 'connect'
    else:
        to_client['message'] = message
        to_client['type'] = 'normal'
    # emit("response", {'data': message['data'], 'username': session['username']}, broadcast=True)
    send(to_client, broadcast=True)

# RESTApi
# Create a URL route in our application for "/"
@app.route('/users/<user_id>’', methods = ['GET', 'POST', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
         userId = request.args.get('user_id')
    if request.method == 'POST':
        data = request.form # a multidict containing POST data
    if request.method == 'DELETE':
        userId = request.args.get('user_id')
    else:
        # Error 405 Method Not Allowed
        None

data = {
    "menu" : "임시",
    "count" : 1,
    "size" : "tall",
    "temp" : "ice"
}

@app.route("/api/hello")
def hello():
    return "Hello world!"

@app.route("/api/order")
def get_order():
    return jsonify({"data" : data, "status" : HTTPStatus.OK})

if __name__ == '__main__':
  socket_io.run(app, debug=True, port=8080)