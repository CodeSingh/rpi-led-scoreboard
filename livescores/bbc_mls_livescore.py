from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from datetime import datetime
import time
from .livescore import Livescore

class BBC_EURO2020_Livescore(Livescore):

    ID = "BBC_MLS"
    NAME = "BBC Major League Soccer"
    LIVESCORE_URL = 'https://www.bbc.co.uk/sport/football/us-major-league/scores-fixtures'

    def __init__(self, team):
        self.team = team

    def get_live_score(self):
        return super().get_live_score()

    def get_all_fixtures(self):
        return super().get_all_fixtures()
