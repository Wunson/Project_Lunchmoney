from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["secret_key"] = "secret!"
socketio = SocketIO(app)

@app.route("/")
def index():
	return render_template("index.html")

@socketio.on("connected")
def connector(data):
    print(data["data"])

if __name__ == "__main__":
    socketio.run(app)
