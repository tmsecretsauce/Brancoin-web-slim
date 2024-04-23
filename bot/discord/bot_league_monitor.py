from datetime import datetime
import dis
from functools import partial, wraps
import random
from sys import prefix
from threading import Thread
import threading
import discord
import asyncio
import discord.ext
import discord.ext.commands
from requests import session
from discord.addbroadcast import AdminAddBroadcast
from discord.repeattimer import RepeatTimer
from discord.addleague import AdminAddLeague
from discord.jackpot import ViewJackpot
from discord.viewmatches import ViewMatches
from discord.coins import Coins
from discord.spin import Spin
from discord.gift import Gift
from discord.coin import Coin
from models.models import Guild, LeagueUser, MatchPlayer, User, Match
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
    commands = [Discover(), Coin(), Gift(), Spin(), Coins(), ViewMatches(), ViewJackpot(), AdminAddLeague(), AdminAddBroadcast()]
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
    #     # self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        for guild in self.guilds:
            self.create_guild(guild)
            self.populate_users(guild)
        open_game_timer = RepeatTimer(130, self.look_for_open_games)
        open_game_timer.start()
        
        closed_game_timer = RepeatTimer(60, self.handle_finished_games)
        closed_game_timer.start()
            

    def populate_users(self, guild: discord.Guild):
        with self.db.Session() as session:
            for member in guild.members:
                    if session.query(User).filter(User.guild_id == str(guild.id), User.user_id == str(member.id)).count() == 0:
                        user = User()
                        user.guild_id = guild.id
                        user.user_id = member.id
                        session.add(user)
                        print("adding new user")
                    else:
                        print("user already exists")
            session.commit()


    def create_guild(self, guild: discord.Guild):
        with self.db.Session() as session:
            if session.query(Guild).filter(Guild.guild_id == str(guild.id)).count() == 0:
                bank = Guild()
                bank.guild_id = guild.id
                bank.brancoins = 10
                session.add(bank)
                session.commit()
            else:
                print("guild entry already exists")

    
    def handle_finished_games(self):
        print("tock")
        with self.db.Session() as session: 
            open_matches = session.query(Match).filter(Match.finished == False).all()
            for open_match in open_matches:
                print("checking if match closed yet")
                if self.league.get_game(open_match) is not None:
                    print("match closed!")
                    open_match.finished = True
                    session.add(open_match)
                    session.commit()
                else:
                    print("match is not closed")

    def look_for_open_games(self):
        print("tick")
        try:
            with self.db.Session() as session:
                trackable_users = session.query(LeagueUser).filter(LeagueUser.trackable == True).all()
                valid_games = self.league.get_valid_games(trackable_users, trackable_users)
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
                    if session.query(Match).filter(Match.match_id == str(match.match_id)).count() == 0:
                        session.add(match)
                        print("adding valid game")
                    else:
                        print("game was already tracked")
                session.commit()

                # we're in a side thread, to output to discord we need to post to the asyncio looper
                asyncio.run_coroutine_threadsafe(self.broadcast_open_matches(), self.loop)

        except Exception as e: 
            print(e)
            print(traceback.format_exc())
    
    async def broadcast_open_matches(self):
        try:
            with self.db.Session() as session:
                open_matches = session.query(Match).filter(Match.finished == False).all()
                for open_match in open_matches:
                    embedVar = await ViewMatches.generate_embed_for_match(open_match, self)
                    await self.broadcast_all(session, embedVar)
        except Exception as e: 
            print(e)
            print(traceback.format_exc())

    async def broadcast_all(self, session, embed):
        guilds = session.query(Guild).filter(Guild.broadcast_channel_id != None).all()
        for guild in guilds:
            broadcast_channel = await self.fetch_channel(guild.broadcast_channel_id)
            await broadcast_channel.send(embed=embed)

    # def wrap(func):
    #     @wraps(func)
    #     async def run(*args, loop=None, executor=None, **kwargs):
    #         if loop is None:
    #             loop = asyncio.get_event_loop()
    #         pfunc = partial(func, *args, **kwargs)
    #         return await loop.run_in_executor(executor, pfunc)
    #     return run


    # async def my_background_task(self):
    #     await self.wait_until_ready()
    #     while not self.is_closed():
    #         print("tick")
    #         self.look_for_open_games()
    #         try:
    #             self.handle_finished_games()
    #         except Exception as e: 
    #             print("failed to process finished game")
    #             print(e)
    #             print(traceback.format_exc())
                   
    #         await asyncio.sleep(120)  # task runs every 60 seconds

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

