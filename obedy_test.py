from flask import Flask, jsonify, render_template
import threading
import logging
import mysql.connector

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

def vydat_obed(karta, stravnik):
    global pocty_obedu
    if stravnik[2] == 1:
        pocty_obedu["jednicky"] -=1
    elif stravnik[2] == 2:
        pocty_obedu["dvojky"] -=1
    else:
        pass

    cursor.execute("UPDATE OBEDY SET STAV=2 WHERE id=%s"% (karta)) #MÍSTO ID DÁT DATA Z KARTY

def pip(karta):
    cursor.execute("SELECT * FROM OBEDY WHERE id=%s"% (karta)) #MÍSTO ID DÁT DATA Z KARTY
    result = cursor.fetchall()
    print(result)
    return (result[0][4], result[0][5], result[0][6], result[0][7])

def reader_loop():
    global stravnici
    while 1:
        karta = input(">>")     #SEM DÁT ČTENÍ KARTY
        if karta == "q":
            break
        if karta:
            stravnik = pip(karta)
            print(stravnik, "pip")
            print(stravnici)
            stravnici.append(stravnik)
            print(stravnici)
            print(len(stravnici))

            #if len(stravnici) > 4:
            #    stravnici.remove(stravnici[0])

            if stravnik[3] == 1:
                print(pocty_obedu, "vydani")
                vydat_obed(karta, stravnik)
                print(pocty_obedu)
                print (stravnici)
            else:
                pass

stravnici = []
print(stravnici, "generate")
pocty_obedu = kolik_obedu()
threading._start_new_thread(reader_loop, ())



app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

@app.route("/")
@app.route("/index")
def index():
    return render_template("test.html")

@app.route("/get_data", methods=["POST", "GET"])
def send_data():
    print(stravnici, pocty_obedu, "sent")
    return jsonify(stravnici, pocty_obedu)
