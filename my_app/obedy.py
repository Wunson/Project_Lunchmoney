from flask import Flask
from flask import render_template
import threading
import mysql.connector

mydb =  mysql.connector.connect(host="localhost",user= "root", passwd= "heslo", db = "obedy_test")
cur = mydb.cursor()

stravnici = []

def pip():
    global stravnici
    while 1:
        karta = input(">>")
        dotaz = f"SELECT * FROM OBEDY WHERE id={karta} "
        cur.execute(dotaz)
        result = cur.fetchall()

        stravnici.append(result[0][4])
        if len(stravnici) > 4:
            stravnici.remove(stravnici[0])

threading._start_new_thread(pip, ())

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    global stravnici
    return render_template("test.html", stravnici = stravnici)
