from dao.singletonDao import Singleton
from datetime import datetime, timedelta
from uuid import uuid4


class MyDB:
    __sql_insert = "INSERT INTO USER (TEL_NUMBER, EMAIL, AUTHENTICATION_KEY, AUTHENTICATION, USER_NAME) VALUES (%s, %s, %s, %s, %s)"
    __sql_insert_blacklist = "INSERT INTO BLACKLIST (ID_USER, ID_COMMAND, CONT, TIME, DESCRIPTION) VALUES (%s, %s, %s, %s, %s)"
    __sql_search_user = "SELECT * FROM USER WHERE TEL_NUMBER = %s"
    _sql_search_commands = "SELECT * FROM COMMANDS"
    __sql_search_user_auth = "SELECT * FROM USER WHERE TEL_NUMBER = %s and AUTHENTICATION = 1"
    __sql_search_commands_user = "SELECT * FROM COMMANDS_USER"
    _sql_insert_commands = "INSERT INTO COMMANDS (COMMANDS_NAME, DESCRIPTION, STATUS) VALUES (%s, %s, %s)"
    _sql_delete_commands = "DELETE FROM COMMANDS WHERE ID = %s"
    __sql_search_blacklist = "SELECT TIME FROM BLACKLIST WHERE ID_USER = %s"
    _sql_search_user_manager = "SELECT * FROM USER_MANAGER WHERE (EMAIL = %s or LOGIN = %s)"
    __sql_update_auth = "UPDATE USER SET AUTHENTICATION = 1 WHERE (TEL_NUMBER = %s and AUTHENTICATION_KEY = %s)"
    __dao = Singleton()
    __cursor = __dao.cursor(buffered=True)

    def deleteCommands(self, command_name) -> bool:
        try:
            self.__cursor.execute(self._sql_delete_commands, (command_name, ))
            self.__dao.commit()
            print(self.__cursor.rowcount, "record(s) deleted")

            return True

        except Exception:
            return False

    def insertCommands(self, command) -> bool:
        try:
            val = (command_name, command_description, command_status)
            self.__cursor.execute(self._sql_insert_commands, val)
            self.__dao.commit()
            print(self.__cursor.rowcount, "record inserted.")

            return True

        except Exception:
            return False

    def searchAllCommands(self) -> list:
        all_commands = []
        try:
            self.__cursor.execute(self._sql_search_commands, )
            results = self.__cursor.fetchall()

            for result in results:
                all_commands.append({
                    'id': result[0],
                    'command_name': result[1],
                    'description': result[2],
                    'status': bool(result[3])
                })

            return all_commands

        except Exception:
            return []

    def searchContBlacklist(self, user_number: str) -> tuple:
        date = ''
        try:
            self.__cursor.execute(
                self.__sql_search_blacklist, (user_number,))
            results = self.__cursor.fetchall()

            for result in results:
                date = result[0].strftime('%d/%m/%y %H:%M:%S')

            return results.__len__(), date

        except Exception as e:
            print(e)
            return -1, 0

    def searchUserManager(self, email: str, login: str) -> tuple:
        try:
            self.__cursor.execute(
                self._sql_search_user_manager, (email, login,))
            results = self.__cursor.fetchall()

            for result in results:
                _, manager_email, manager_login, manager_password = result

            return (manager_login, manager_email, manager_password)

        except Exception as e:
            print(e)
            return ()

    def insertCommand(self, cel_number: str, auth: str) -> bool:
        val = (cel_number, "pedro.cassiano@sou.fae.br", auth, "Pedrin")
        try:
            self.__cursor.execute(self.__sql_insert, val)
            self.__dao.commit()
            print(self.__cursor.rowcount, "record inserted.")
            return True

        except Exception:
            return False

    def insertBlackList(self, cel_number: str, command: int, description: str) -> tuple:
        cont, _ = self.searchContBlacklist(cel_number)
        print(f'CONTTTTTTTTTTTT {cont}')
        now = datetime.today()

        dt_string = now + timedelta(minutes=cont + 1)

        if cont > 2:
            dt_string = dt_string + timedelta(days=999999)

        val = (cel_number, command, cont, dt_string, description)
        try:
            self.__cursor.execute(self.__sql_insert_blacklist, val)
            self.__dao.commit()
            print(self.__cursor.rowcount, "record inserted.")

            return (True, cont)

        except Exception as e:
            print(e)
            return (False, 0)

    def insertUser(self, user_number: str, user_email, user_name: str) -> str:
        auth = uuid4()
        print(str(auth))
        val = (user_number, user_email, str(auth), False, user_name)
        try:
            self.__cursor.execute(self.__sql_insert, val)
            self.__dao.commit()
            print(self.__cursor.rowcount, "record inserted.")
            return str(auth)

        except Exception as e:
            print(e)
            return 'False'

    def checkUser(self, user_id) -> bool:
        print(user_id)
        try:
            self.__cursor.execute(self.__sql_search_user, (user_id,))
            results = self.__cursor.fetchall()

            if not results:
                return False

            return True

        except Exception as e:
            print(e)
            return False

    def searchCommands(self) -> list:
        all_commands = []
        try:
            self.__cursor.execute(self.__sql_search_commands_user, )
            results = self.__cursor.fetchall()

            for i in results:
                all_commands.append(
                    {'commands': i[3], 'prompt': i[4], 'datetime': i[5]})

            print(all_commands)
            return all_commands

        except Exception as e:
            print(e)
            return []

    def checkAuth(self, user_id) -> bool:
        try:
            self.__cursor.execute(self.__sql_search_user_auth, (user_id,))
            results = self.__cursor.fetchall()

            if not results:
                return False

            return True

        except Exception as e:
            print(e)
            return False

    def authUser(self, user_id: str, token: str) -> bool:
        try:
            print(token)
            self.__cursor.execute(self.__sql_update_auth, (user_id, token,))
            self.__dao.commit()

            print(self.__cursor.rowcount, "record(s) affected")

            if self.__cursor.rowcount > 0:
                return True

            return False

        except Exception as e:
            print(f'authUser Error: {e}')
            return False
