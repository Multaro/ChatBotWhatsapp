import mysql.connector

class Connection:

    def __init__(self):
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password=""
        )
        
        print(mydb)