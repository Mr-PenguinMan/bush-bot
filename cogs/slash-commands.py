from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord.ext import commands

import discord

class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.slash = SlashCommand(client, override_type=True)

        @self.slash.slash(name="ping")
        async def _ping(ctx: SlashContext):
            embed = discord.Embed(color=discord.Colour.from_rgb(255, 130, 53))
            embed.add_field(name="**Ping**", value=f":table_tennis: Pong! {self.client.latency * 1000} ms")
            await ctx.send(embeds=[embed])

    def cog_unload(self):
        self.slash.remove()


def setup(bot):
    bot.add_cog(Slash(bot))