import mysql.connector

mydb =  mysql.connector.connect(host="localhost",user= "root", passwd= "heslo", db = "obedy_test")

cur = mydb.cursor()

karta = 1

dotaz = f"SELECT * FROM OBEDY WHERE id={karta} "

cur.execute(dotaz)

result = cur.fetchall()

print(result)

input()

mydb.close()
