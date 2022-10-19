
import os
# import threading
import logging
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response
from twilio.rest import Client
from command import Command
from commands import Commands
from dao.dao import MyDB
from utils.mail import SendMail
from utils.cursedwords import CursedWords
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


load_dotenv('.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/yagoc/Documents/Python/ChatBotWhatsapp/manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    mail = db.Column(db.String(50))
    password = db.Column(db.String(50))


with app.app_context():
    db.create_all()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'access-tokens' in request.headers:
            token = request.headers['access-tokens']

        if not token:
            return jsonify({'message': 'token válido não encontrado'})

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Users.query.filter_by(
                login=data['login']).first()

        except Exception:
            return jsonify({'message': 'token inválida'})

        return f(current_user, *args, **kwargs)
    return decorator


account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('BOT_TOKEN')

client = Client(account_sid, auth_token)

cursedwords = CursedWords()
cursed_words = cursedwords.readerCursedWords()

commands = Commands()


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
        if '/token' not in command.getBody():
            return '🚨 É necessário autentificar o usuário. 🚨'

        token = command.getBody().split('/token')
        res = mydb.authUser(command.getUser(), token[1].strip())

        if not res:
            return '❌ Falha ao autentificar usuário! ❌'

        return '✅ Usuário autentificado! ✅\nPara obter todos os comandos use: /help'

    if checkPenalization != '':
        # Formatando para comparar com a data atual.
        checkPenalization_comp = datetime.datetime.strptime(
            checkPenalization, '%d/%m/%y %H:%M:%S')
        command_time = datetime.datetime.now()

        if checkPenalization_comp > command_time:
            return f'❌ Usuário penalizado até {checkPenalization}. ❌'

    if '/' not in command.getBody():
        return '❌ Comando não encontrado ❌\nPara obter todos os comandos use: /help'

    body = (command.getBody().split('/')[1]).split(' ')
    user_commands = body[0]
    print(len(body))
    user_prompt = body[1] if len(body) > 1 else None
    print(user_prompt)

    if user_prompt in cursed_words:
        # ALTERAR ID
        cert, cont = mydb.insertBlackList(
            command.getUser(), commands.selectCommand(user_commands)['id'],
            user_prompt)
        print(f'CERT : {cert}')
        return '🚨 Não é permitido buscas no contexto +18 ou violência. 🚨'

    elif user_commands:
        return commands.responseCommand(user_commands, user_prompt)

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


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    try:
        user = Users.query.filter_by(login=data['login']).first()
        print(f'USER {user}')

        if user:
            return jsonify({'message': 'login ou email já cadastrado'})

        hashed_password = generate_password_hash(
            data['password'], method='sha256')

        new_user = Users(login=data['login'], mail=data['mail'],
                         password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'registrado com sucesso'})

    except Exception:
        return jsonify({'message': 'erro ao cadastrar usuário'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():

    auth = request.authorization
    print(auth)

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Users.query.filter_by(login=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'login': user.login, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()

    result = []

    for user in users:
        user_data = {}
        user_data['login'] = user.login
        user_data['mail'] = user.mail
        user_data['password'] = user.password

        result.append(user_data)

    return jsonify({'users': result, 'manager': ''})


@app.route('/cursedwords', methods=['GET', 'POST'])
def getCursedWords():
    cursedwords_list = cursedwords.readerCursedWords()
    if request.method == 'GET':
        if not cursedwords_list:
            return jsonify({'message': 'error'})
        return jsonify(cursedwords_list)

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if cursedwords.writeCursedWords(json, cursedwords_list):
            # ATUALIZAR A LISTA GLOBAL
            cursed_words = cursedwords.readerCursedWords()
            print(cursed_words)
            return jsonify(cursed_words)
        return jsonify({'message': 'error'})
    else:
        return jsonify({'message': 'Content-Type not supported!'})


@app.route('/commands', methods=['GET', 'POST'])
@token_required
def getCommands(current_user):
    if request.method == 'GET':
        commands_response = commands.getCommands()

        if not commands:
            return jsonify({'message': 'nenhum comando existente'})

        print(commands.getCommands())
        return jsonify({'manager': current_user.login, 'commands': commands_response})

    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json = request.get_json()
        if commands.incrementCommands(json):
            return jsonify({'message': 'comando inserido com sucesso!'})

        return jsonify({'message': 'falha ao inserir comando'})
    else:
        return 'Content-Type not supported!'


@app.route('/commands/<command_name>', methods=['DELETE'])
@token_required
def delete_author(current_user, command_name):
    if not commands.deleteCommands(id):
        return jsonify({'message': 'falha ao excluir comando'})

    return jsonify({'manager': current_user.login, 'message': 'excluido com sucesso!'})
