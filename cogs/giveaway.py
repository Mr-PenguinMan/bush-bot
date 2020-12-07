from discord.ext.commands import has_permissions
from discord.ext.commands import command
from discord.ext.commands import group
from discord.ext import commands
import discord


class Giveaways(commands.Cog):

    def __init__(self, client):
        self.client = client


    @group(name="giveaway", aliases=["ga", "raffle"], invoke_without_command = True, ignore_extra = False)
