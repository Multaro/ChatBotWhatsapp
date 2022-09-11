from dao.singletonDao import Singleton


class MyDB:
    __sql_insert = "INSERT INTO USER (TEL_NUMBER, EMAIL, AUTHENTICATION_KEY, USER_NAME) VALUES (%s, %s, %s, %s)"
    __dao = Singleton()
    __cursor = __dao.cursor()

    def insertCommand(self, cel_number: str, auth: str) -> bool:
        val = (cel_number, "pedro.cassiano@sou.fae.br", auth, "Pedrin")
        try:
            self.__cursor.execute(self.__sql_insert, val)
            self.__dao.commit()
            print(self.__cursor.rowcount, "record inserted.")
            return True

        except Exception:

            return False
