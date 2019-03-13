from flask import Flask, jsonify, render_template
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

def kolik_obedu():
    cursor.execute("SELECT COUNT(*) FROM OBEDY WHERE cislo_obedu=1 AND stav=1")
    jednicky = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM OBEDY WHERE cislo_obedu=2 AND stav=1")
    dvojky = cursor.fetchall()
    return {"jednicky":jednicky[0][0], "dvojky":dvojky[0][0]}

def vydat_obed(stravnik, karta):
    global pocty_obedu
    print("vydano")
    if stravnik[2] == 1:
        pocty_obedu["jednicky"] -=1
    elif stravnik[2] == 2:
        pocty_obedu["dvojky"] -=1
    else:pass

    cursor.execute("UPDATE OBEDY SET STAV=2 WHERE jmeno=%s"% (karta)) #MÍSTO ID DÁT DATA Z KARTY

def in_time(range, cas):
    pred = (range[0][0] > cas[0]) or ((range[0][0] == cas[0]) and (range[0][1] > cas[1]))
    po =   (range[1][0] < cas[0]) or ((range[1][0] == cas[0]) and (range[1][1] < cas[1]))
    return not (pred or po)

def what_day(num):
    days = ("po", "ut", "st", "ct", "pa", "so", "ne")
    return days[num]

def je_prestavka(cas, rozvrhy):
    for doba in rozvrhy["prestavky"].values():
        return in_time(doba, cas)

    return False

def kontrola(stravnik, karta):
    cas = localtime(time())
    day = what_day(cas.tm_wday)
    cas = (cas.tm_hour,cas.tm_min)
    cas = (12,25)

    with open("rozvrhy.json", "r") as json_data:
        rozvrhy = json.load(json_data)

    if stravnik[3] != 1:
        print("nemá") # + píp
    else:
        prestavka = rozvrhy["1A"][day]
        doba = rozvrhy["prestavky"]["2"]
        if in_time(doba, cas):
            vydat_obed(stravnik, karta)
        else:
            if je_prestavka(cas, rozvrhy):
                print("ven!")

            else:
                vydat_obed(stravnik, karta)

def pip(karta):
    cursor.execute("SELECT * FROM OBEDY WHERE id=%s"% (karta)) #MÍSTO ID DÁT DATA Z KARTY
    result = cursor.fetchall()
    return (result[0][4], result[0][5], result[0][6], result[0][7])

def reader_loop():
    global stravnici
    while 1:
        karta = input(">>")     #SEM DÁT ČTENÍ KARTY
        if karta == "q":
            break
        elif karta:
            stravnik = pip(karta)
            stravnici.append(stravnik)

            print(stravnik, "pip")
            print(stravnici)

            if len(stravnici) > 4:
                stravnici.remove(stravnici[0])

            kontrola(stravnik, karta)

stravnici = []
print(stravnici, "generate")
pocty_obedu = kolik_obedu()
threading._start_new_thread(reader_loop, ())

app = Flask(__name__)

log = logging.getLogger('werkzeug') # just for testing
log.disabled = True
app.logger.disabled = True

@app.route("/")
@app.route("/index")
def index():
    return render_template("test.html")

@app.route("/get_data", methods=["POST", "GET"])
def send_data():
    #print(stravnici, pocty_obedu, "sent")
    return jsonify(stravnici, pocty_obedu)
