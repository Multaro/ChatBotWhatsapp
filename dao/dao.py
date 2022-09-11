from dao.singletonDao import Singleton


class MyDB:
    __sql_insert = "INSERT INTO USER (TEL_NUMBER, EMAIL, AUTHENTICATION_KEY, USER_NAME) VALUES (%s, %s, %s, %s)"
    __dao = Singleton()
    __cursor = __dao.cursor()

    def insertCommand(self) -> bool:
        val = ("19993070538", "pedro.cassiano@sou.fae.br", "ASDS545D", "Pedrin")
        try:
            self.__cursor.execute(self.__sql_insert, val)
            self.__dao.commit()
            print(self.__cursor.rowcount, "record inserted.")
            return True

        except:
            return False
