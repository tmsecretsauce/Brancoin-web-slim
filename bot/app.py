import discord
from discord.ext import commands
from sqlalchemy import create_engine, select
import discord.bot_client
import discord.bot_league_monitor
from models.dbcontainer import DbContainer, DbService
from models.models import LeagueUser
from league.leagueservice import LeagueService
from envvars import Env
from dependency_injector.wiring import Provide, inject
from league.leaguecontainer import LeagueContainer



@inject
def main(dbservice: DbService = Provide[DbContainer.service], league_service: LeagueService = Provide[LeagueContainer.service]):
    with dbservice.Session() as session:
        statement = select(LeagueUser)
        john = session.scalars(statement).first()




container = LeagueContainer()
container.init_resources()
container.wire(modules=[__name__])


container2 = DbContainer()
container2.init_resources()
container2.wire(modules=[__name__])

# main()

# discord.bot_client.run_bot()
monitor = discord.bot_league_monitor.run()