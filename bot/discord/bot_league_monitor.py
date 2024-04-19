import dis
import random
from sys import prefix
import discord
import asyncio
import discord.ext
import discord.ext.commands
from discord.coin import Coin
from models.models import User
from discord.discover import Discover
from league.leaguecontainer import LeagueContainer
from models.dbcontainer import DbContainer, DbService
from league.leagueservice import LeagueService
from dependency_injector.wiring import Provide
from envvars import Env
from discord.ext import commands

class DiscordMonitorClient(commands.Bot):
    commands = [Discover(), Coin()]
    def __init__(self, intents, dbservice: DbService = Provide[DbContainer.service], league_service: LeagueService = Provide[LeagueContainer.service]):
        super().__init__(intents=intents, command_prefix="bran ")
        self.db = dbservice
        self.league = league_service

    async def on_message(self, message):
        if message.author == self.user:
            return
        for command in self.commands:
            await command.process(message, self.db)
        await super().on_message(message)

    # async def setup_hook(self) -> None:
    #     # create the background task and run it in the background
    #     self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        try:
            with self.db.Session() as session:
                for guild in self.guilds:
                    for member in guild.members:
                        print(member.name)
                        user = User()
                        user.guild_id = guild.id
                        user.user_id = member.id
                        session.add(user)
                session.commit()
        except:
            print("An exception occurred")


    # async def my_background_task(self):
    #     await self.wait_until_ready()
    #     while not self.is_closed():
    #         await channel.send(counter)
    #         await asyncio.sleep(60)  # task runs every 60 seconds

def run():

    container = LeagueContainer()
    container.init_resources()
    container.wire(modules=[__name__])

    container2 = DbContainer()
    container2.init_resources()
    container2.wire(modules=[__name__])

    itnent = discord.Intents.default()
    itnent.members = True
    itnent.message_content  = True
    client = DiscordMonitorClient(intents=itnent)

    client.run(Env.discord_token)

