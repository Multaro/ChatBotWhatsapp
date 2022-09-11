
import os
import threading
import logging
from dotenv import load_dotenv
from flask import Flask, request
from twilio.rest import Client
from command import Command
from dao.dao import MyDB

load_dotenv('.env')

app = Flask(__name__)

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('BOT_TOKEN')

client = Client(account_sid, auth_token)


def __threadRespond(command):
    mydb = MyDB()
    if mydb.insertCommand(command.getUser(), command.getBody()):

        client.messages.create(
            from_=command.getBot(),
            body=command.getBody(),
            to=command.getUser()
        )

        logging.info('Message Delivered')


@app.route('/message', methods=['POST'])
def reply():
    print(request.form.get('Body').lower())
    from_ = request.form.get('From')
    to = request.form.get('To')
    message = request.form.get('Body').lower()

    if message:
        command = Command(from_, message, to)
        thread = threading.Thread(target=__threadRespond, args=(command,))
        thread.start()
        return '200'


@app.route('/user', methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'
