class Command:
    def __init__(self, user: str, body: str, bot: str):
        self.user = user
        self.body = body
        self.bot = bot
        print(self.user, self.body, self.bot)
        # self.args = args
        # self.command = command
