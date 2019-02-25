from flask import Flask, jsonify, render_template
import threading
import mysql.connector

mydb = mysql.connector.connect(host="localhost", \
                                user="root", \
                                passwd="heslo", \
                                db="obedy_test")
cursor = mydb.cursor()

def kolik_obedu():
    cursor.execute("SELECT COUNT(*) FROM OBEDY WHERE cislo_obedu=1")
    jednicky = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM OBEDY WHERE cislo_obedu=2")
    dvojky = cursor.fetchall()

    return {"jednicky":jednicky[0][0], "dvojky":dvojky[0][0]}

def pip():
    global stravnici
    global obedy
    stravnici = []
    while 1:
        karta = input(">>")
        if karta == "q":
            break
        if karta:
            cursor.execute(f"SELECT * FROM OBEDY WHERE id={karta}")
            result = cursor.fetchall()

            stravnik = (result[0][4], result[0][5], result[0][6])
            stravnici.append(stravnik)
            if len(stravnici) > 4:
                stravnici.remove(stravnici[0])

            cursor.execute(f"UPDATE OBEDY SET STAV=2 WHERE ID={karta}")

            if stravnik[2] == 1:
                obedy["jednicky"] -=1
            elif stravnik[2] == 2:
                obedy["dvojky"] -=1

obedy = kolik_obedu()
threading._start_new_thread(pip, ())



app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("test.html")

@app.route("/get_data", methods=["POST", "GET"])
def send_data():
    return jsonify(stravnici, obedy)
