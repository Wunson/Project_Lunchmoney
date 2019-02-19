from flask import Flask, jsonify, render_template
import threading
import mysql.connector

mydb =  mysql.connector.connect(host="localhost",user= "root", passwd= "heslo", db = "obedy_test")
cursor = mydb.cursor()

def pip():
    global stravnici
    stravnici = []
    while 1:
        karta = input(">>")
        if karta == "q":
            break
        if karta:
            dotaz = f"SELECT * FROM OBEDY WHERE id={karta}"
            cursor.execute(dotaz)
            result = cursor.fetchall()

            stravnik = (result[0][4], result[0][5], result[0][6])
            stravnici.append(stravnik)
            if len(stravnici) > 4:
                stravnici.remove(stravnici[0])

threading._start_new_thread(pip, ())


app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("test.html")

@app.route("/get_data", methods = ["POST", "GET"])
def send_data():
    global starvnici
    return jsonify(stravnici)
