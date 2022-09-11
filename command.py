class Command:
    __user = ''
    __body = ''
    __bot = ''

    def __init__(self, user: str, body: str, bot: str):
        self.__user = user
        self.__body = body
        self.__bot = bot

    def getUser(self) -> str:
        return self.__user

    def getBody(self) -> str:
        return self.__body

    def getBot(self) -> str:
        return self.__bot
