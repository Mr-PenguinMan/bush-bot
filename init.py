from discord.ext import commands

import discord
import jishaku
import json

def get_prefix(client, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefix = prefixes.get(str(message.guild.id), "m!")

	return [prefix, "bush "]

class BushBot(commands.Bot):

    async def is_owner(self, user):
        return user.id in [322862723090219008, 785526919516651561]

    
	def run(self, token=None):
		if token is None:
			with open("auth.json") as w:
				token = json.load(w)["TOKEN"]
			self.run(token)

		else:
			super().run(token)


# Credit to SirNapkin1334#7960 for this spaghetti code
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
