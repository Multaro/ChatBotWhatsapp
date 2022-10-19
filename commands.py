from dao.dao import MyDB


class Commands:
    _all_commands = []
    _mydb = None

    def __init__(self) -> None:
        self._mydb = MyDB()
        self.__updateCommands()

    def responseCommand(self, user_command, user_prompt) -> str:
        print(f'userprompt {self._all_commands}')
        c = self.selectCommand(user_command)
        print(f'TESTE: {c}')
        if c['command_name'] == 'help':
            if not user_prompt:
                return c['description']

            c = self.selectCommand(user_prompt)
            return c['description']

        if c['status']:
            # AQUI VAI FICAR OS COMANDOS
            return 'em construção'
        return f"🚨 Comando /{c['command_name']} desabilitado"

        # if not help_message:
        #    return '🚨 Comando não existe'

    def __updateCommands(self):
        self._all_commands = self._mydb.searchAllCommands()

    def getCommands(self) -> list:
        return self._all_commands

    def selectCommand(self, command_name):
        return next((c for c in self._all_commands if c['command_name'] == command_name), '🚨 Comando não encontrado')

    def deleteCommands(self, id) -> bool:
        if self._mydb.deleteCommands(id):
            self.__updateCommands()
            return True
        return False

    def incrementCommands(self, new_commands) -> bool:
        def verifyCommand(command_name) -> bool:
            print(f'COMMANDO ENTRADO: {command_name}')
            for find_name in self._all_commands:
                print(find_name['command_name'])
                if command_name == find_name['command_name']:
                    return False
            return True

        if isinstance(new_commands, dict):
            if verifyCommand(new_commands['command_name']):
                if self._mydb.insertCommands(new_commands['command_name'], new_commands['description'], new_commands['status']):
                    self._all_commands.append(new_commands)
                    return True
                return False
            return False

        for command in new_commands:
            if verifyCommand(command['command_name']):
                if self._mydb.insertCommands(command['command_name'], command['description'], command['status']):
                    self._all_commands.append(command)
        return True
