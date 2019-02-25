import mysql.connector

mydb = mysql.connector.connect(host="localhost", \
                                user="root", \
                                passwd="heslo", \
                                db="obedy_test")
cursor = mydb.cursor()
cursor.execute("UPDATE OBEDY SET STAV=1 WHERE STAV=2")
