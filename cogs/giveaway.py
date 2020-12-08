from discord.ext.commands import has_permissions
from discord.ext.commands import command
from discord.ext.commands import group
from discord.ext import commands
import datetime
import asyncio
import discord


def convert(time: str): # There is definitely a better way to do this
    units = ["s", "m", "h", "d"]

    conversions = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 3600*24,
    }

    if time[-1] not in units:
        return 420

    try:
        number = int(time[:-1])

    except:
        return 69

    return number * conversions[time[-1]]


async def create_question_embeds(questions: list):
    x = []
    y = 0
    for q in questions:
        y += 1

        embed = discord.Embed(color = disord.Colour.from_rgb(255, 150, 53))
        embed.add_field(name = f"Question {y}", value = f"{q}")

        x.append(embed)

    return x


class Giveaways(commands.Cog):

    def __init__(self, client):
        self.client = client


    @group(name="giveaway", aliases=["ga", "raffle"], invoke_without_command = True, ignore_extra = False)
    async def bush_giveaway(self, ctx):
        await ctx.send("Giveaway command activated")


    @bush_giveaway.command(name="create", aliases=["start"])
    async def create_giveaway(self, ctx):
        start_embed = discord.Embed(color = disord.Colour.from_rgb(255, 150, 53))
        start_embed.add_field(name = "Giveaway creation process started.", value = "Answer the questions within 30 seconds or L")
		start_embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by: {ctx.author.name}")

        e = [
            "List the channel the giveaway shall commence in",
            "List the duration of the giveaway (accepts seconds, minutes, hours, and days)",
            "What will the reward be?"
        ]
        
        a = []

        def authorAndChannelCheck(message):
            return message.channel == ctx.channel and message.author == ctx.author 

        to_send = await create_question_embeds(e)

        for x in to_send:
            await ctx.send(embed=x)

            try:
                asd = await self.client.wait_for('message', timeout = 30.0, check = check)

            except asyncio.TimeoutError:
                embed = discord.Embed(color = disord.Colour.from_rgb(255, 150, 53))
                embed.add_field(name = "Timed Out", value = "<:disagree:767758599916486717> You took too long, L")

            else:
                a.append(asd) 


def setup(client):
	client.add_cog(Giveaways(client))