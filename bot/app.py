from datetime import datetime
import discord
from sqlalchemy import create_engine, select
import discord.bot_league_monitor
from models.dbcontainer import DbContainer, DbService
from models.models import LeagueUser, Match, MatchPlayer
from league.leagueservice import LeagueService
from dependency_injector.wiring import Provide, inject
from league.leaguecontainer import LeagueContainer
from envvars import Env


@inject
def main(dbservice: DbService = Provide[DbContainer.service], league_service: LeagueService = Provide[LeagueContainer.service]):
    with dbservice.Session() as session:
        # print(league_service.api_riot_watcher.account.by_riot_id("americas", "BofaJoeMamas", "0001"))
        # print(league_service.api_riot_watcher.account.by_riot_id("americas", "AwkwardPandas", "NA1"))
        statement = select(Match).filter(Match.finished == False)
        john = session.scalars(statement).first()
        print(john)
        print(league_service.get_game(john))
        # print(league_service.is_in_game(john))
        # print(league_service.get_valid_game(john, [john]))

        

# if Env.is_debug == False:
#     import alembic.config
#     alembicArgs = [
#         '--raiseerr',
#         'upgrade', 'head',
#     ]
#     alembic.config.main(argv=alembicArgs)


container = LeagueContainer()
container.init_resources()
container.wire(modules=[__name__])


container2 = DbContainer()
container2.init_resources()
container2.wire(modules=[__name__])


# main()

monitor = discord.bot_league_monitor.run()