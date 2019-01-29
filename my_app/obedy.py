from flask import Flask
from flask import render_template
import threading
import mysql.connector
import json

mydb =  mysql.connector.connect(host="localhost",user= "root", passwd= "heslo", db = "obedy_test")
cursor = mydb.cursor()

wipe = []
with open("stravnici.json", "w") as f:
    json.dump(wipe, f)

def pip():
    stravnici = []
    while 1:
        karta = input(">>")
        if karta == "q":
            break
        if karta:
            dotaz = f"SELECT * FROM OBEDY WHERE id={karta}"
            cursor.execute(dotaz)
            result = cursor.fetchall()

            stravnik = (result[0][4],result[0][5], result[0][6])
            stravnici.append(stravnik)
            if len(stravnici) > 4:
                stravnici.remove(stravnici[0])

            with open("stravnici.json", "w") as f:
                json.dump(stravnici, f)


threading._start_new_thread(pip, ())

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    with open("stravnici.json", "r") as f:
        stravnici = json.load(f)

    return render_template("index.html", stravnici = stravnici)
