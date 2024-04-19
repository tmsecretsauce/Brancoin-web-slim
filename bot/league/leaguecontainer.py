
from dependency_injector import containers, providers

from league.leagueservice import LeagueService
from riotwatcher import LolWatcher
from envvars import Env

class LeagueContainer(containers.DeclarativeContainer):
    api_client = providers.Singleton(
        LolWatcher,
        api_key=Env.league_token,
    )

    service = providers.Factory(
        LeagueService,
        lol_watcher=api_client
    )