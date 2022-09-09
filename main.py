
import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.rest import Client
from Command import Command

load_dotenv('.env')

app = Flask(__name__)

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('BOT_TOKEN')

client = Client(account_sid, auth_token)

def respond(to, from_, message) -> str:
    client.messages.create(
        from_=from_,
        body='Successfull',
        to=to
    )
    return 'Successfull'


@app.route('/message', methods=['POST'])
def reply():
    from_ = request.form.get('From')
    to = request.form.get('To')
    message = request.form.get('Body').lower()

    command = Command(from_, message, to)

    if message:
        return respond(from_, to, message)

@app.route('/user', methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'