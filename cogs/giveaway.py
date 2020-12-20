from discord.ext.commands.cog import listener
from discord.ext.commands import has_permissions
from discord.ext.commands import command
from discord.ext.commands import group
from discord.ext import commands

import datetime
import asyncio
import discord
import re

def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('minute',      60),
        ('second',      1)
    ]

    strings=[]
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value , seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)

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
        raise ValueError("Invalid time provided")
    nowtime = datetime.datetime.now()
    endtime = datetime.datetime.now()
    for result in times:
        if result[1] in datealiases["weeks"]:
            endtime = endtime + datetime.timedelta(days=int(result[0])*7)
        elif result[1] in datealiases["days"]:
            endtime = endtime + datetime.timedelta(days=int(result[0]))
        elif result[1] in datealiases["hours"]:
            endtime = endtime + datetime.timedelta(hours=int(result[0]))
        elif result[1] in datealiases["minutes"]:
            endtime = endtime + datetime.timedelta(minutes=int(result[0]))
        elif result[1] in datealiases["seconds"]:
            endtime = endtime + datetime.timedelta(seconds=int(result[0]))
        else:
            raise ValueError("Somehow got a time value that wasn't the preset lengths.")
    return {'endtime': endtime, 'readable': td_format(endtime - nowtime)}


async def create_question_embeds(questions: list):
    x = {}
    y = 0
    for q in questions:
        y += 1

        embed = discord.Embed(color = discord.Colour.from_rgb(255, 150, 53))
        embed.add_field(name = f"Question {y}", value = f"{q}")

        x[q] = embed

    return x


class Giveaways(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.active_giveaways = []
        self.active_giveaway_message = None


    @group(name="giveaway", aliases=["ga", "raffle"], invoke_without_command = True, ignore_extra = False)
    async def bush_giveaway(self, ctx):
        await ctx.send("Giveaway command activated. Use 'm!giveaway create' or 'm!ga create' to create a giveaway.")


    @bush_giveaway.command(name="create --role ", aliases=["start -r ", "start --role ", "create -r "])
    async def create_giveaway_with_role_req(self, ctx, role: discord.Role):
        start_embed = discord.Embed(color = discord.Colour.from_rgb(255, 150, 53))
        start_embed.add_field(name = "Giveaway creation process started.", value = "Answer the questions within 30 seconds or L")
        start_embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by: {ctx.author.name}")
        
        answers = []

        def authorAndChannelCheck(message):
            return message.channel == ctx.channel and message.author == ctx.author 

        questions = await create_question_embeds([
            "List the channel the giveaway shall commence in",
            "List the duration of the giveaway (accepts seconds, minutes, hours, days, and weeks)",
            "What will the reward be?"
        ])

        for message in questions:
            await ctx.send(embed=questions[message])

            try:
                response = await self.client.wait_for('message', timeout = 30.0, check = authorAndChannelCheck)

            except asyncio.TimeoutError:
                embed = discord.Embed(color = discord.Colour.from_rgb(255, 150, 53))
                embed.add_field(name = "Timed Out", value = "<:disagree:767758599916486717> You took too long, L")

            else:
                if message == "List the channel the giveaway shall commence in":
                    try:
                        parsed_response = await commands.TextChannelConverter().convert(ctx, response.content)
                    except commands.errors.ChannelNotFound:
                        return await ctx.send(embed=discord.Embed(title="Invalid channel", description="Could not convert the text given to a text channel in the current server"))
                elif message == "List the duration of the giveaway (accepts seconds, minutes, hours, days, and weeks)":
                    try:
                        parsed_response = convert(response.content)
                    except ValueError as e:
                        return await ctx.send(embed=discord.Embed(title="Invalid time provided", description=str(e)))
                elif message == "What will the reward be?":
                    parsed_response = response.content
                answers.append(parsed_response)

        ends_at = answers[1]["endtime"].strftime(r"%A, %b %d %Y, at %I:%M%p")
        self.active_giveaways.append(answers[1]["endtime"])
                
        confirmation_embed = discord.Embed(title="Is this correct?", color=discord.Colour.from_rgb(255, 150, 53))
        confirmation_embed.add_field(name="Channel", value=answers[0].mention)
        confirmation_embed.add_field(name="Length", value=answers[1]["readable"])
        confirmation_embed.add_field(name="Ends at", value=ends_at)
        confirmation_embed.add_field(name="Reward", value=answers[2])
        await ctx.send(embed=confirmation_embed)

        target_channel = discord.utils.get(ctx.guild.text_channels, answers[0].name)
        giveaway_embed = discord.Embed(title= f"Giveaway",color = discord.Colour.from_rgb(255, 150, 53))
        giveaway_embed.add_field(name = "Hosted By", value = f"{ctx.author.mention}")
        giveaway_embed.add_field(name = "Reward", value = f"{reward}")
        giveaway_embed.set_footer(icon_url = ctx.guild.icon_url, text = f"Ends at {ends_at}")

        sent = await target_channel.send(embed=giveaway_embed)
        sent.add_reaction("🎉") # TODO: Set up listener to watch for reactions and filter out ones that do not qualify.

        giveaway_cfg = {
            "required_role": role,
            "message": sent
        }

        self.active_giveaway_message = giveaway_cfg 



    @listener
    async def on_raw_reaction_add(payload):
        if payload.message.id == self.active_giveaway_message.id and payload.emoji = "🎉": # TODO: Convert `self.active_giveaway_message` to a list when I'm feeling less lazy 
            if self.active_giveaway_message["required_role"] in payload.member.roles:
                pass
            else:
                


def setup(client):
    client.add_cog(Giveaways(client))
