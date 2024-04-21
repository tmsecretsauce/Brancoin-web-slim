from functools import lru_cache
import json
from os import name
import os
from riotwatcher import LolWatcher, RiotWatcher
import riotwatcher
from riotwatcher.LolWatcher import MatchApiV5

from models.models import LeagueUser

class LeagueService():
    region_riot_api = "americas"
    region_lol = "NA1"

    def __init__(self, lol_watcher: LolWatcher, riot_watcher: RiotWatcher) -> None:
        self.api_riot_watcher = riot_watcher
        self.api_lol_watcher = lol_watcher
        self.api_match : MatchApiV5 = lol_watcher.match

    # todo: worth using memcached here instead? probably not tbh... but it's a nice thought.
    @lru_cache(maxsize=20)
    def get_puuid(self, league_user: LeagueUser):
        return self.api_riot_watcher.account.by_riot_id(region=self.region_riot_api, game_name=league_user.summoner_name, tag_line=league_user.tag)['puuid']
    
    def get_puuids(self, league_users: list[LeagueUser]):
        return map(lambda x: (x, self.get_puuid(x)), league_users)

    def get_matches(self, league_user: LeagueUser):
        return self.api_match.matchlist_by_puuid(self.region_lol, self.get_puuid(league_user))
    
    def get_valid_game(self, league_user: LeagueUser, trackable_users: list[LeagueUser]):
        print("get valid game for " )
        try:
            spectator_data = self.api_lol_watcher.spectator.by_summoner(self.region_lol, self.get_puuid(league_user))
        except: 
            return None
        print ("got active game for " )

        if(spectator_data['gameMode'] != "ARAM"):
            print("Not an aram")
            return None

        user_participant = list(map(lambda user: {'league_user': user, 'participant_json': self.find_participant(user, spectator_data['participants'])}, trackable_users)) 
        valid_participants = list(filter(lambda x: x['participant_json'] is not None, user_participant))

        if len(valid_participants) > 1:
            return {
                'spectator_data': spectator_data,
                'valid_participants': valid_participants
            }
        else: 
            print("Not enough valid players")
            return None
    
    def get_valid_games(self, league_users: list[LeagueUser], trackable_users: list[LeagueUser]):
        all_valid_games = list(filter(lambda x: x is not None, map(lambda league_user: self.get_valid_game(league_user, trackable_users), league_users)))
        unique_valid_games = {x['spectator_data']['gameId']: x for x in all_valid_games}.values()
        return unique_valid_games
    
    def champ_id_to_name(self, search_id):
        with open(os.path.dirname(__file__) + '/champion.json') as fp:
            champion_data = json.load(fp)
            for attribute, value in champion_data['data'].items():
                if value['key'] == str(search_id):
                    return attribute
        return "Unknown"    
            

    def find_participant(self, user_to_find: LeagueUser, participants_to_search): 
        return next(filter(lambda participant: participant['puuid'] == self.get_puuid(user_to_find), participants_to_search), None)