from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    stravnici = [
    {"jmeno" : "Jakub Vašíček",
    "trida" : "4B",
    "obed" : "n",
    "rozvrh" : True
    },
    {"jmeno" : "Kryštof Stejskal",
    "trida" : "4B",
    "obed" : "1",
    "rozvrh" : True
    },
    {"jmeno" : "Lucie Čechová",
    "trida" : "3B",
    "obed" : "2",
    "rozvrh" : False
    }
    ]

    return render_template("index.html", stravnici = stravnici)
