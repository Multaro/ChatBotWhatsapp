from dao.connection import mydb


class Singleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = mydb
        return cls.__instance
