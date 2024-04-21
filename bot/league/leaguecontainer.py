
from dependency_injector import containers, providers

from league.leagueservice import LeagueService
from riotwatcher import LolWatcher, RiotWatcher
from envvars import Env

class LeagueContainer(containers.DeclarativeContainer):
    api_client = providers.Singleton(
        LolWatcher,
        api_key=Env.league_token,
    )

    riot_api_client = providers.Singleton(
        RiotWatcher,
        api_key=Env.league_token,
    )

    service = providers.Factory(
        LeagueService,
        lol_watcher=api_client,
        riot_watcher=riot_api_client
    )