
from dotenv import load_dotenv
from flask import Flask, request
from twilio.rest import Client
from Command import Command

load_dotenv()

app = Flask(__name__)

account_sid = 'ACaede7a7f585ae1c0273ff467bd13b78b'
auth_token = '582fa7f0c97dce2db70608764b262fdb'

client = Client(account_sid, auth_token)

print(client.account_sid)


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
