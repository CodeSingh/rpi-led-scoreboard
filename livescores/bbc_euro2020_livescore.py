from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from datetime import datetime
import time
from .livescore import Livescore

class BBC_EURO2020_Livescore(Livescore):

    ID = "BBC_EURO2020"
    NAME = "BBC Euro 2020"
    LIVESCORE_URL = 'https://www.bbc.co.uk/sport/football/european-championship/scores-fixtures'

    def __init__(self, team):
        self.team = team

    def get_live_score(self):
        return super().get_live_score()

    def get_all_fixtures(self):
        return super().get_all_fixtures()
