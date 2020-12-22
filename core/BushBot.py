from discord.ext import commands

class BushBot(commands.Bot):

    async def is_owner(self, user):
        return user.id in vars.OWNERS

    
    def run(self, token=None):
        if token is None:
            with open("auth.json") as w:
                token = json.load(w)["TOKEN"]
            self.run(token)

        else:
            super().run(token)

