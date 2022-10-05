
import os
# import threading
import logging
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from twilio.rest import Client
from command import Command
# from commands import Commands
from dao.dao import MyDB
from utils.mail import SendMail
from utils.cursedwords import CursedWords


load_dotenv('.env')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('BOT_TOKEN')

client = Client(account_sid, auth_token)

cursedwords = CursedWords()
global cursed_words
cursed_words = cursedwords.readerCursedWords()


def __respond(command) -> str:
    mydb = MyDB()
    checkUser = mydb.checkUser(command.getUser())
    checkAuth = mydb.checkAuth(command.getUser())
    _, checkPenalization = mydb.searchContBlacklist(command.getUser())

    print(checkUser, checkAuth)

    if not checkUser:
        if '/login' in command.getBody():
            (name, mail) = command.getBody().split('/login')[1].split(',')
            name.strip()
            mail.strip()
            print(f'name: {name}\nmail: {mail}')
            auth = mydb.insertUser(command.getUser(), mail, name)

            if auth != 'False':
                SendMail(mail, auth)
                return '🚨 Token de verificação enviado ao email cadastrado. 🚨'

        return '🚨 Usuário não identificado. 🚨\nUse o seguinte comando: "/login <nome>, <e-mail>"\nExemplo: /login Pedro Miguel, pedromiguel@hotmail.com.'

    if not checkAuth:
        if not '/token' in command.getBody():
            return '🚨 É necessário autentificar o usuário. 🚨'

        token = command.getBody().split('/token')
        res = mydb.authUser(command.getUser(), token[1].strip())

        if not res:
            return '❌ Falha ao autentificar usuário! ❌'

        return '✅ Usuário autentificado! ✅\nPara obter todos os comandos use: /help'

    if checkPenalization != '':
        # Formatando para comparar com a data atual.
        checkPenalization_comp = datetime.strptime(
            checkPenalization, '%d/%m/%y %H:%M:%S')
        command_time = datetime.now()

        if checkPenalization_comp > command_time:
            return f'🚨 Usuário penalizado até {checkPenalization}. 🚨'

    if not '/' in command.getBody():
        return '❌ Comando não encontrado ❌\nPara obter todos os comandos use: /help'

    body = (command.getBody().split('/')[1]).split(' ')
    user_commands = body[0]
    print(len(body))
    user_prompt = body[1] if len(body) > 1 else None
    print(user_prompt)

    print(cursed_words)

    if user_prompt in cursed_words:
        cert, cont = mydb.insertBlackList(command.getUser(), 1, user_prompt)
        print(f'CERT : {cert}')
        return '🚨 Não é permitido buscas no contexto +18 ou violência. 🚨'

    elif 'help' in user_commands:
        return 'Em construção'

    elif 'championships' in user_commands:
        # colocar insert do comando
        print(user_prompt)

    elif 'live' in user_commands:
        # colocar insert do comando
        print(user_prompt)

    elif 'table' in user_commands:
        # colocar insert do comando
        print(user_prompt)

    else:
        return '❌ Comando não encontrado ❌\nPara obter todos os comandos use: /help'

    logging.info('Message Delivered')


@app.route('/message', methods=['POST'])
def reply():
    print(request.form.get('Body').lower())
    from_ = request.form.get('From')
    to = request.form.get('To')
    message = request.form.get('Body').lower()

    if message:
        command = Command(from_, message, to)
        msg = __respond(command)

        client.messages.create(
            from_=command.getBot(),
            body=msg,
            to=command.getUser()
        )

        # Com threads
        # thread = threading.Thread(target=__threadRespond, args=(command,))
        # thread.start()
        return '200'


@app.route('/datas', methods=['GET'])
def json_example():
    mydb = MyDB()
    datas = jsonify(mydb.searchCommands())
    return datas


@app.route('/user', methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'


@app.route('/cursedwords', methods=['GET', 'POST'])
def getCursedWords():
    cursedwords_list = cursedwords.readerCursedWords()
    if request.method == 'GET':
        if not cursedwords_list:
            return 'Error'
        return jsonify(cursedwords_list)

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if cursedwords.writeCursedWords(json, cursedwords_list):
            # ATUALIZAR A LISTA GLOBAL
            cursed_words = cursedwords.readerCursedWords()
            print(cursed_words)
            return jsonify(cursed_words)
        return 'Error'
    else:
        return 'Content-Type not supported!'
