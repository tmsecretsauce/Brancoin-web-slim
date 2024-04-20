import dis
import random
from sys import prefix
import discord
import asyncio
import discord.ext
import discord.ext.commands
from discord.spin import Spin
from discord.gift import Gift
from discord.coin import Coin
from models.models import User
from discord.discover import Discover
from league.leaguecontainer import LeagueContainer
from models.dbcontainer import DbContainer, DbService
from league.leagueservice import LeagueService
from dependency_injector.wiring import Provide, inject
from envvars import Env
from discord.ext import commands
import traceback


@inject
class DiscordMonitorClient(commands.Bot):
    commands = [Discover(), Coin(), Gift(), Spin()]
    def __init__(self, intents, dbservice: DbService = Provide[DbContainer.service], league_service: LeagueService = Provide[LeagueContainer.service]):
        super().__init__(intents=intents, command_prefix="b ")
        self.db = dbservice
        self.league = league_service

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        for command in self.commands:
            try:
                await command.process(self.get_context, message, self.db)
            except Exception as e: 
                print(e)
                print(traceback.format_exc())
        if message.content.startswith("bran help"):
            await self.help(message)
        await super().on_message(message)

    async def help(self, message: discord.Message):
        output = "All commands: "
        for command in self.commands:
            if hasattr(command, 'usage'):
                output = output + f"\n {command.usage}"
        await message.reply(output)

    # async def setup_hook(self) -> None:
    #     # create the background task and run it in the background
    #     self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        for guild in self.guilds:
            try:
                with self.db.Session() as session:
                    bank = User()
                    bank.guild_id = guild.id
                    bank.user_id = "jackpot"
                    bank.brancoins = 0
                    session.add(bank)
                    session.commit()
            except:
                print("jackpot already exists")

            for member in guild.members:
                try:
                    with self.db.Session() as session:
                        user = User()
                        user.guild_id = guild.id
                        user.user_id = member.id
                        session.add(user)
                        session.commit()
                except:
                    print("user already exists")


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

    print(f"Debug: {Env.is_debug}")
    client.run(Env.active_discord_token)

