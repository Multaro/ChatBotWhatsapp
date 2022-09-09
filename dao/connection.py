import mysql.connector

class Connection:
    def __init__(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword",
            database="mydatabase"
        )
        
        print(mydb)