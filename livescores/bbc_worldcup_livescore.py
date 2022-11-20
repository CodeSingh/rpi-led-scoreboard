from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from datetime import datetime
import time
from .livescore import Livescore

class BBC_WORLDCUP_Livescore(Livescore):

    ID = "BBC_WORLDCUP"
    NAME = "BBC World Cup"
    LIVESCORE_URL = 'https://www.bbc.co.uk/sport/football/world-cup/scores-fixtures'

    def __init__(self, team):
        self.team = team

    def get_live_score(self):
        return super().get_live_score()

    def get_all_fixtures(self):
        return super().get_all_fixtures()
