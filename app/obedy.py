from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
from time import localtime, time, sleep
import threading
from playsound import playsound
import mysql.connector
import json
import serial


mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                passwd="heslo",
                                db="obedy_test")
cursor = mydb.cursor()

app = Flask(__name__)
app.config["secret_key"] = "secret!"
socketio = SocketIO(app)
thread = None
schedule_check = 0

ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM4'

def get_lunch_amount():
    cursor.execute("SELECT COUNT(*) FROM OBEDY WHERE cislo_obedu=1 AND stav=1")
    ones = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM OBEDY WHERE cislo_obedu=2 AND stav=1")
    twos = cursor.fetchall()
    amount = {"ones":ones[0][0], "twos":twos[0][0]}
    return amount

def in_time(range, my_time):
    before = (range[0][0] > my_time[0]) or ((range[0][0] == my_time[0]) and (range[0][1] > my_time[1]))
    after =   (range[1][0] < my_time[0]) or ((range[1][0] == my_time[0]) and (range[1][1] < my_time[1]))
    return not (before or after)

def what_day(num):
    days = ("po", "ut", "st", "ct", "pa", "so", "ne")
    if num > 4:
        return "po"
    return days[num]

def break_time(my_time, schedule_table):
    for lunchbreak in schedule_table["breaks"]:
        if in_time(schedule_table["breaks"][lunchbreak], my_time):
            return lunchbreak
    return False

def dispence_lunch(consumer, card_id, lunch_amount):
    print("Lunch dispenced")
    cursor.execute("UPDATE OBEDY SET STAV=2 WHERE id=%s"% (card_id)) #MÍSTO ID DÁT DATA Z KARTY
    if consumer[2] == 1:
        lunch_amount["ones"] -=1
        playsound("audio/one.wav")
    elif consumer[2] == 2:
        lunch_amount["twos"] -=1
        playsound("audio/two.wav")
    else:pass

    socketio.emit("update_amounts", lunch_amount)

def check(consumer, card_id, lunch_amount):
    current_time = localtime(time())
    day = what_day(current_time.tm_wday)
    current_time = (current_time.tm_hour,current_time.tm_min)
    # current_time = (12,25) #pryč s tím
    print(current_time, day)

    with open("schedule.json", "r") as json_data:
        schedule_table = json.load(json_data)

    miss_schedule = False
    if consumer[3] != 1:
        print("NO LUNCH") # + píp
        playsound("audio/no.wav")
    else:
        if schedule_check:
            print("checking schedule")
            lunchbreak = break_time(current_time, schedule_table)
            if lunchbreak:
                if consumer[1] in schedule_table[day][lunchbreak]:
                    print("On time")
                    dispence_lunch(consumer, card_id, lunch_amount)
                else:
                    print("GET OUT")
                    playsound("audio/miss.wav")
                    miss_schedule = True
            else:
                print("Here you go")
                dispence_lunch(consumer, card_id, lunch_amount)
        else:
            print("Here you go")
            dispence_lunch(consumer, card_id, lunch_amount)

    print("sending consumer data")
    socketio.emit("card_swipe", {"consumer":consumer, "card_id":card_id, "miss_schedule":miss_schedule})

def card_swipe(card_id):
    cursor.execute("SELECT * FROM OBEDY WHERE id=%s"% (card_id)) #MÍSTO ID DÁT DATA Z KARTY
    result = cursor.fetchall()
    return (result[0][4], result[0][5], result[0][6], result[0][7])

def reader_loop(lunch_amount):
    ser.open()
    while 1:
        card_id = ser.readline()
        card_id = str(card_id, 'utf-8')
        if card_id:
            consumer = card_swipe(card_id)
            print(consumer)
            check(consumer, card_id, lunch_amount)

lunch_amount = get_lunch_amount()
threading._start_new_thread(reader_loop, (lunch_amount, ))

@app.route("/")
@app.route("/index")
def index():
    return render_template("table.html")

@app.route("/rozvrhy")
def interface():
    with open("schedule.json", "r") as json_data:
        schedule_table = json.load(json_data)

    return render_template("rozvrhy.html", schedule_table=schedule_table)

@socketio.on("approved")
def disspenced(data):
    print("deviant approoved")
    dispence_lunch(data["consumer"], data["card_id"], lunch_amount)

@socketio.on("switch_schedule")
def switch_schedule(setting):
    global schedule_check
    schedule_check = setting
    print("schedule check: ", schedule_check)

@socketio.on("schedule_change")
def update_schedule(data):
    print("schedule updated")
    with open("schedule.json", "w") as json_data:
        json.dump(data["data"], json_data)

@socketio.on("login")
def login(passwd):
    print("Recived password: ", passwd)
    if passwd == "nozkeus":
        socketio.emit("authenticate", passwd)

@socketio.on("connected")
def connector(data):
    print(data["data"])
    socketio.emit('update_amounts', lunch_amount)

if __name__ == "__main__":
    socketio.run(app)
