import mysql.connector
import json

mydb =  mysql.connector.connect(host="localhost",user= "root", passwd= "heslo", db = "obedy_test")
cursor = mydb.cursor()

stravnici = []

while 1:
    karta = input(">>")
    if karta == "q":
        break
    if karta:
        dotaz = f"SELECT * FROM OBEDY WHERE id={karta} "
        cursor.execute(dotaz)
        result = cursor.fetchall()

        stravnik = (result[0][4],result[0][5], result[0][6])
        stravnici.append(stravnik)
        if len(stravnici) > 4:
            stravnici.remove(stravnici[0])

        with open("stravnici.json", "w") as f:
            json.dump(stravnici, f)
