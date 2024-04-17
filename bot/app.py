import discord
from discord.ext import commands
from sqlalchemy import create_engine
from models import Base
from envvars import Env

engine = create_engine(Env.db_conn_str, echo=True)


intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='b ', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

print("lol")
print(Env.db_conn_str)
print(Base.metadata.sorted_tables)

bot.run(Env.discord_token)