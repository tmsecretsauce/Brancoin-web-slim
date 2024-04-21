from datetime import datetime
import dis
import random
from sys import prefix
import discord
import asyncio
import discord.ext
import discord.ext.commands
from discord.addleague import AdminAddLeague
from discord.jackpot import ViewJackpot
from discord.viewmatches import ViewMatches
from discord.coins import Coins
from discord.spin import Spin
from discord.gift import Gift
from discord.coin import Coin
from models.models import Jackpot, LeagueUser, MatchPlayer, User, Match
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
    commands = [Discover(), Coin(), Gift(), Spin(), Coins(), ViewMatches(), ViewJackpot(), AdminAddLeague()]
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

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        for guild in self.guilds:
            try:
                with self.db.Session() as session:
                    bank = Jackpot()
                    bank.guild_id = guild.id
                    bank.brancoins = 10
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


    async def my_background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            print("tick")
            try:
                with self.db.Session() as session:
                    trackable_users = session.query(LeagueUser).filter(LeagueUser.trackable == True).all()
                    print(trackable_users)
                    valid_games = self.league.get_valid_games(trackable_users, trackable_users)
                    print(valid_games)
                    for valid_game in valid_games:
                        print("valid game found")
                        match = Match()
                        match.finished = False
                        match.match_id = valid_game['spectator_data']['gameId']
                        match.start_time = datetime.now()
                        for participant in valid_game['valid_participants']:
                            match_player = MatchPlayer()
                            match_player.league_user = participant['league_user']
                            match_player.champion = self.league.champ_id_to_name(participant['participant_json']['championId'])
                            match.match_players.append(match_player)
                        session.add(match)
                        session.commit()
            except Exception as e: 
                print("failed to find valid game")
                print(e)
                print(traceback.format_exc())

            await asyncio.sleep(60)  # task runs every 60 seconds

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

