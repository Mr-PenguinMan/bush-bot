from discord.ext.commands import command
from discord.ext.commands import check
from contextlib import redirect_stdout
import io, textwrap, traceback, os
from discord.ext import commands
from termcolor import cprint
import discord



async def is_owner(ctx):
	return ctx.author.id in [322862723090219008, 785526919516651561]


class Administration(commands.Cog):
	"""Administration Commands"""

	def __init__(self, client):
		self.client = client

	@command(hidden=True, aliases=["kill"])
	async def logout(self, ctx):
		"""Shuts down bot"""
		if ctx.author.id in owners:
			await self.client.logout()

		else: 
			await ctx.send("<:disagree:767758599916486717> You are not one of my owners and therefore are incapable of ameliorating yourself to the stations required to operate this command.")

	# Copyright (c) 2015 Rapptz - Modified Slightly
	@command(hidden=True, name="eval")
	@check(is_owner)
	async def _eval(self, ctx, *, body):
		"""Evaluates code"""

		env = {
			"self": self,
			"client": self.client,
			"ctx": ctx
		}

		env.update(globals())

		if body.startswith("```") and body.endswith("```"):
			body = "\n".join(body.split("\n")[1:-1])

		else:
			body = body.strip("` \n")
		stdout = io.StringIO()

		to_compile = f"""import discord, os, math, sys, asyncio, json, re
async def func():\n{textwrap.indent(body, "  ")}"""

		try:
			exec(to_compile, env)

		except Exception as e:
			val = f"```py\n{e.__class__.__name__}: {e}\n```"
			embed = discord.Embed(color=discord.Colour.from_rgb(255, 150, 53))
			embed.add_field(name="Traceback", value=val)
			embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Evaluator: {ctx.author.name}")
			return await ctx.send(embed=embed)

		func = env["func"]

		try:
			with redirect_stdout(stdout):
				ret = await func()

		except Exception:
			value = stdout.getvalue()
			embed = discord.Embed(color=discord.Colour.from_rgb(255, 130, 53))
			embed.add_field(name="Exception", value=f"```py\n{value}{traceback.format_exc()}\n```")
			embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Evaluator: {ctx.author.name}")
			await ctx.send(embed=embed)

		else:
			value = stdout.getvalue()

			try:
				await ctx.message.add_reaction("\u2705")

			except:
				pass

			if ret is None:
				if value:
					embed = discord.Embed(color=discord.Colour.from_rgb(255, 130, 53))
					embed.add_field(name="Output", value=f"```py\n{value}\n```")
					embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Evaluator: {ctx.author.name}")

					await ctx.send(embed=embed)

			else:
				self._last_result = ret
				embed = discord.Embed(color=discord.Colour.from_rgb(255, 130, 53))
				embed.add_field(name="Output", value=f"```py\n{value}{ret}\n```")
				embed.add_field(name="Return Type", value=f"```py\n{type(ret)}\n```", inline=False)
				embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Evaluator: {ctx.author.name}")

				await ctx.send(embed=embed)
					
	# End Copyright Notice


def setup(client):
	client.add_cog(Administration(client))
