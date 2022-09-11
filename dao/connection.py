import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'bot',
    'port': 3306,
    'raise_on_warnings': True
}

print('instanciado')

mydb = mysql.connector.connect(**config)
