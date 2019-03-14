from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
from time import localtime, time
import threading
import logging
import mysql.connector
import json

mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                passwd="heslo",
                                db="obedy_test")
cursor = mydb.cursor()

app = Flask(__name__)
app.config["secret_key"] = "secret!"
socketio = SocketIO(app)

def kolik_obedu():
    cursor.execute("SELECT COUNT(*) FROM OBEDY WHERE cislo_obedu=1 AND stav=1")
    jednicky = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM OBEDY WHERE cislo_obedu=2 AND stav=1")
    dvojky = cursor.fetchall()
    pocet = {"jednicky":jednicky[0][0], "dvojky":dvojky[0][0]}
    return pocet

def in_time(range, cas):
    print(range, cas)
    pred = (range[0][0] > cas[0]) or ((range[0][0] == cas[0]) and (range[0][1] > cas[1]))
    po =   (range[1][0] < cas[0]) or ((range[1][0] == cas[0]) and (range[1][1] < cas[1]))
    return not (pred or po)

def what_day(num):
    days = ("po", "ut", "st", "ct", "pa", "so", "ne")
    return days[num]

def je_prestavka(cas, rozvrhy):
    for doba in rozvrhy["prestavky"].values():
        if in_time(doba, cas):
            return True
    return False

def vydat_obed(stravnik, karta, pocty_obedu):
    print("vydano")
    cursor.execute("UPDATE OBEDY SET STAV=2 WHERE id=%s"% (karta)) #MÍSTO ID DÁT DATA Z KARTY
    if stravnik[2] == 1:
        pocty_obedu["jednicky"] -=1
    elif stravnik[2] == 2:
        pocty_obedu["dvojky"] -=1
    else:pass

    socketio.emit('vydany_obed', pocty_obedu)

def kontrola(stravnik, karta, pocty_obedu):
    cas = localtime(time())
    day = what_day(cas.tm_wday)
    cas = (cas.tm_hour,cas.tm_min)
    cas = (12,25) #pryč s tím
    print(cas, day)

    with open("rozvrhy.json", "r") as json_data:
        rozvrhy = json.load(json_data)

    if stravnik[3] != 1:
        print("nemá") # + píp
    else:
        prestavka = rozvrhy["1A"][day] #pryč s tím
        doba = rozvrhy["prestavky"][prestavka]
        if in_time(doba, cas):
            print("cas")
            vydat_obed(stravnik, karta, pocty_obedu)
        else:
            if je_prestavka(cas, rozvrhy):
                socketio.emit("a_ven", {"stravnik":stravnik, "karta":karta})
                print("ven!")
            else:
                print("else")
                vydat_obed(stravnik, karta, pocty_obedu)

def pip(karta):
    cursor.execute("SELECT * FROM OBEDY WHERE id=%s"% (karta)) #MÍSTO ID DÁT DATA Z KARTY
    result = cursor.fetchall()
    return (result[0][4], result[0][5], result[0][6], result[0][7])

def reader_loop(stravnici, pocty_obedu):
    while 1:
        karta = input(">>")     #SEM DÁT ČTENÍ KARTY
        if karta == "q":
            break
        elif karta:
            stravnik = pip(karta)
            stravnici.append(stravnik)

            print(stravnik, "pip")

            if len(stravnici) > 4:
                stravnici.remove(stravnici[0])

            socketio.emit("pip", stravnici)

            kontrola(stravnik, karta, pocty_obedu)

stravnici = []
print(stravnici, "generate")
pocty_obedu = kolik_obedu()
threading._start_new_thread(reader_loop, (stravnici, pocty_obedu))

@app.route("/")
@app.route("/index")
def index():
    return render_template("table.html")

@socketio.on("vydano")
def vydano(data):
    vydat_obed(data["stravnik"], data["karta"], pocty_obedu)

@socketio.on("connected")
def connector(data):
    print(data["data"])
    socketio.emit("connection_established", data)
    socketio.emit('vydany_obed', pocty_obedu)
    socketio.emit("pip", stravnici)
