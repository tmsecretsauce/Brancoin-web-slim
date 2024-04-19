from functools import lru_cache
from riotwatcher import LolWatcher
from riotwatcher.LolWatcher import MatchApiV5

from models.models import LeagueUser

class LeagueService():
    def __init__(self, lol_watcher: LolWatcher) -> None:
        self.api_lol_watcher = lol_watcher
        self.api_match : MatchApiV5 = lol_watcher.match

    # todo: worth using memcached here instead? probably not tbh... but it's a nice thought.
    @lru_cache(maxsize=20)
    def get_puuid(self, league_user: LeagueUser):
        return self.api_lol_watcher.summoner.by_name(league_user.region, league_user.summoner_name)['puuid']

    def get_matches(self, league_user: LeagueUser):
        return self.api_match.matchlist_by_puuid(league_user.region, self.get_puuid(league_user))
    
    def is_in_game(self, league_user: LeagueUser):
        return self.api_lol_watcher.spectator.by_summoner(league_user.region, self.get_puuid(league_user))