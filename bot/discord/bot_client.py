import discord
from envvars import Env
from discord.ext import commands

def run_bot():
    intents = discord.Intents.default()
    intents.messages = True
    bot = commands.Bot(command_prefix='b ', intents=intents)

    @bot.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    bot.run(Env.discord_token)