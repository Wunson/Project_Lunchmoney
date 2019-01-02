from flask import Flask
from flask import render_template
import threading

stravnici = []

def pip():
    global stravnici
    while 1:
        stravnici.append(input(">>"))
        if len(stravnici) > 4:
            stravnici.remove(stravnici[0])

threading._start_new_thread(pip, ())

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    global stravnici
    return render_template("test.html", stravnici = stravnici)
