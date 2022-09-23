from dao.singletonDao import Singleton
from uuid import uuid4


class MyDB:
    __sql_insert = "INSERT INTO USER (TEL_NUMBER, EMAIL, AUTHENTICATION_KEY, AUTHENTICATION, USER_NAME) VALUES (%s, %s, %s, %s, %s)"
    __sql_search_user = "SELECT * FROM USER WHERE TEL_NUMBER = %s"
    __sql_search_user_auth = "SELECT * FROM USER WHERE TEL_NUMBER = %s and AUTHENTICATION = 1"
    __sql_update_auth = "UPDATE USER SET AUTHENTICATION = 1 WHERE (TEL_NUMBER = %s and AUTHENTICATION_KEY = %s)"
    __dao = Singleton()
    __cursor = __dao.cursor(buffered=True)

    def insertCommand(self, cel_number: str, auth: str) -> bool:
        val = (cel_number, "pedro.cassiano@sou.fae.br", auth, "Pedrin")
        try:
            self.__cursor.execute(self.__sql_insert, val)
            self.__dao.commit()
            print(self.__cursor.rowcount, "record inserted.")
            return True

        except Exception:
            return False

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

    def checkAuth(self, user_id) -> bool:
        print(user_id)
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
        print(user_id)
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
