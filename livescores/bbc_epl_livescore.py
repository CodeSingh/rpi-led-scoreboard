from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import time
import requests
from .livescore import Livescore

class BBC_EPL_Livescore(Livescore):

    ID = "BBC_EPL"
    NAME = "BBC English Premier League"
    LIVESCORE_URL = 'https://www.bbc.co.uk/sport/football/premier-league/scores-fixtures/'

    def __init__(self, team):
        self.team = team

    def get_live_score(self):
        return super().get_live_score()

    def get_all_fixtures(self):
        return super().get_all_fixtures()