
import os
import threading
import logging
from dotenv import load_dotenv
from flask import Flask, request
from twilio.rest import Client
from command import Command
from dao.dao import MyDB
# from utils.mail import SendMail

load_dotenv('.env')

app = Flask(__name__)

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('BOT_TOKEN')

client = Client(account_sid, auth_token)


def __threadRespond(command):
    mydb = MyDB()
    checkUser = mydb.checkUser(command.getUser())
    checkAuth = mydb.checkAuth(command.getUser())

    print(checkUser, checkAuth)

    if checkUser:
        if checkAuth:
            if '/help' in command.getBody():
                client.messages.create(
                    from_=command.getBot(),
                    body='Em construção',
                    to=command.getUser()
                )
        else:
            if '/token' in command.getBody():
                token = command.getBody().split('/token')
                res = mydb.authUser(command.getUser(), token[1].strip())
                if res:
                    client.messages.create(
                        from_=command.getBot(),
                        body='✅ Usuário autentificado! ✅\nPara obter todos os comandos use: /help',
                        to=command.getUser()
                    )
                else:
                    client.messages.create(
                        from_=command.getBot(),
                        body='❌ Falha ao autentificar usuário! ❌',
                        to=command.getUser()
                    )
            else:
                client.messages.create(
                    from_=command.getBot(),
                    body='🚨 É necessário autentificar o usuário. 🚨',
                    to=command.getUser()
                )

    elif '/login' in command.getBody():
        (name, mail) = command.getBody().split('/login')[1].split(',')
        name.strip()
        mail.strip()
        print(f'name: {name}\nmail: {mail}')
        auth = mydb.insertUser(command.getUser(), mail, name)

        if auth != 'False':
            # SendMail('yago.cassiano@hotmail.com', auth)
            client.messages.create(
                from_=command.getBot(),
                body=f'Use: /token {auth}',
                to=command.getUser()
            )

    else:
        client.messages.create(
            from_=command.getBot(),
            body='🚨 Usuário não identificado. 🚨\nUse o seguinte comando: "/login <nome>, <e-mail>"\nExemplo: /login Pedro Miguel, pedromiguel@hotmail.com.',
            to=command.getUser()
        )
    # if command.getBody == '/login'
    '''
    if mydb.insertCommand(command.getUser(), command.getBody()):

        client.messages.create(
            from_=command.getBot(),
            body=command.getBody(),
            to=command.getUser()
        )
    '''

    logging.info('Message Delivered')


@ app.route('/message', methods=['POST'])
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


@ app.route('/user', methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'
