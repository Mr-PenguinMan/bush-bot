from discord.ext.commands import has_permissions
from discord.ext.commands import command
from discord.ext.commands import group
from discord.ext import commands
import re
import datetime
import asyncio
import discord

dateregex = re.compile(r"(?:(\d+)(d(?:ays?)?|h(?:ours?|rs?)?|m(?:inutes?|ins?)?|s(?:econds?)?|w(?:eeks?|ks?)?)(?: |$))", flags=re.I)
datealiases = {
    'weeks': ('w', 'weeks', 'week', 'wk', 'wks'),
    'days': ('d', 'days', 'day'),
    'hours': ('h', 'hours', 'hour', 'hr', 'hrs'),
    'minutes': ('m', 'min', 'mins', 'minutes', 'minute'),
    'seconds': ('s', 'seconds', 'second')
}
def convert(time: str):
    times = dateregex.findall(time)
    if len(times) < 1:
        raise ValueError("Invalid input provided")
    currtime = datetime.datetime.now()
    for result in times:
        if result[1] in datealiases["weeks"]:
            currtime = currtime + datetime.timedelta(days=int(result[0])*7)
        elif result[1] in datealiases["days"]:
            currtime = currtime + datetime.timedelta(days=int(result[0]))
        elif result[1] in datealiases["hours"]:
            currtime = currtime + datetime.timedelta(hours=int(result[0]))
        elif result[1] in datealiases["minutes"]:
            currtime = currtime + datetime.timedelta(minutes=int(result[0]))
        elif result[1] in datealiases["seconds"]:
            currtime = currtime + datetime.timedelta(seconds=int(result[0]))
        else:
            raise ValueError("Somehow got a time value that wasn't the preset lengths.")
    return currtime


async def create_question_embeds(questions: list):
    x = []
    y = 0
    for q in questions:
        y += 1

        embed = discord.Embed(color = discord.Colour.from_rgb(255, 150, 53))
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
        start_embed = discord.Embed(color = discord.Colour.from_rgb(255, 150, 53))
        start_embed.add_field(name = "Giveaway creation process started.", value = "Answer the questions within 30 seconds or L")
        start_embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by: {ctx.author.name}")
        
        answers = []

        def authorAndChannelCheck(message):
            return message.channel == ctx.channel and message.author == ctx.author 

        questions = await create_question_embeds([
            "List the channel the giveaway shall commence in",
            "List the duration of the giveaway (accepts seconds, minutes, hours, and days)",
            "What will the reward be?"
        ])

        for message in questions:
            await ctx.send(embed=message)

            try:
                response = await self.client.wait_for('message', timeout = 30.0, check = authorAndChannelCheck)

            except asyncio.TimeoutError:
                embed = discord.Embed(color = discord.Colour.from_rgb(255, 150, 53))
                embed.add_field(name = "Timed Out", value = "<:disagree:767758599916486717> You took too long, L")

            else:
                answers.append(response) 


def setup(client):
    client.add_cog(Giveaways(client))
