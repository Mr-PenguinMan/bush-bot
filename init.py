from discord.ext import commands
from termcolor import cprint
from core import BushBot
from utils import vars

import discord
import jishaku
import time
import json
import os


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefix = prefixes.get(str(message.guild.id), "m!")

    return [prefix, "bush "]


cprint("Initializing bot...", "green", attrs=["bold"])
bg1 = time.perf_counter_ns()

intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True, typing=False, presences=False, bans=True, dm_messages=False)

client = BushBot(command_prefix=get_prefix, case_insensitive=True, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))

# Credit to SirNapkin1334#7960 for this spaghetti code
# It might be terrible to read but it looks amazing when you run it
if __name__ == "__main__": 
    cprint("Loading extensions...", "green", attrs=["bold"]) 
    failed = True 
    g1 = time.perf_counter_ns() 
    for extension in sorted([f"cogs.{x.decode().replace('.py', '')}" for x in os.listdir(os.fsencode("cogs")) if \
    x.decode() not in vars.NOT_COGS] + ["jishaku"]): # iterate over files in cogs directory & clean up & add jishaku
        try:
            t1 = time.perf_counter_ns()
            client.load_extension(extension)
            t2 = time.perf_counter_ns()
        except Exception as e:
            cprint("\n" if failed else "" + f"Failed:  {extension}:{':'.join(str(e).split(':')[1:])}", "red")
            failed = True
        else:
            cprint(f"{'Loading: ' if failed else ' ' * 9}{extension} ({(t2-t1)/1000.0}µs)", "green")
            failed = False
    g2 = time.perf_counter_ns()
    cprint(f"Finished loading extensions in {(g2-g1)/1000000.0}ms", "green", attrs=["bold"])

@client.event
async def on_ready():
	global bg1
	cprint(f"Logged in as @{client.user} ({client.user.id})", "green", attrs=["bold"])
	bg2 = time.perf_counter_ns()
	cprint(f"Finished initialization in {(bg2-bg1)/1000000.0}ms!", "green", attrs=["bold"])
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The bush"))

@client.event
async def on_command_error(ctx, error):
    if not isinstance(error, discord.ext.commands.errors.CommandNotFound):
            embed = discord.Embed(color=discord.Colour.from_rgb(255, 150, 53))
            embed.add_field(name="Error when running command", value=f"```{error} ```")

            await ctx.send(embed=embed)

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "m!"

    with open("prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=4)


client.run()