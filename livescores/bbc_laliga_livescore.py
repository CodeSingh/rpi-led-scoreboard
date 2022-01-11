from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from datetime import datetime
import time
from .livescore import Livescore

class BBC_LALIGA_Livescore(Livescore):

    ID = "BBC_LALIGA"
    NAME = "BBC Spanish La Liga"
    LIVESCORE_URL = 'https://www.bbc.co.uk/sport/football/spanish-la-liga/scores-fixtures/'

    def __init__(self, team):
        self.team = team

    def get_live_score(self):
        return super().get_live_score()

    def get_all_fixtures(self):
        return super().get_all_fixtures()
