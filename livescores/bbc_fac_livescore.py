from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import time
from .livescore import Livescore

class BBC_EPL_Livescore(Livescore):

    ID = "BBC_FAC"
    NAME = "BBC English FA Cup"

    def __init__(self, team):
        self.team = team

    def get_live_score(self):
    
        self.LIVESCORE_URL = 'https://www.bbc.co.uk/sport/football/fa-cup/scores-fixtures/'

        self.now = datetime.now() # current date and time
        self.url = self.LIVESCORE_URL + '?' + self.now.strftime("%Y%m%d%h%M%s")
        self.page = urlopen(self.url)
        self.soup = BeautifulSoup(self.page.read(), "lxml")

        self.my_fixture = {}
        self.my_fixture["team-home"] = 'default'
        self.my_fixture["team-away"] = 'default'
        self.my_fixture["score-home"] = 0
        self.my_fixture["score-away"] = 0
        self.my_fixture["status"] = 'No Game'
        self.my_fixture["start-time"] = ""

        self.all_fixtures = self.soup.find_all("li", class_="gs-o-list-ui__item gs-u-pb-")  
        if self.all_fixtures:
            for self.fixture in self.all_fixtures:
                if self.team in self.fixture.text:
                    if self.fixture.find("span", class_="sp-c-fixture__team-name--home"): # Started
                        self.my_fixture["team-home"] = self.fixture.find("span", class_="sp-c-fixture__team-name--home") \
                                                .find("span", class_="qa-full-team-name").text
                        self.my_fixture["team-away"] = self.fixture.find("span", class_="sp-c-fixture__team-name--away") \
                                                .find("span", class_="qa-full-team-name").text
                        self.my_fixture["score-home"] = self.fixture.find("span", class_="sp-c-fixture__number--home").text
                        self.my_fixture["score-away"] = self.fixture.find("span", class_="sp-c-fixture__number--away").text
                        if self.fixture.find("span", class_="sp-c-fixture__status"):
                            self.my_fixture["status"] = self.fixture.find("span", class_="sp-c-fixture__status").text.split(" ",1)[0] + "'"
                        else:
                            self.my_fixture["status"] = ""

                        if self.fixture.find("span", class_="sp-c-fixture__number--time"):
                            self.my_fixture["start-time"] = self.fixture.find("span", class_="sp-c-fixture__number--time").text
                        else:
                            self.my_fixture["start-time"] = ""
                
                        return self.my_fixture
                    else:
                        self.my_fixture["team-home"] = self.fixture.find("span", class_="sp-c-fixture__team--time-home") \
                                                .find("span", class_="qa-full-team-name").text
                        self.my_fixture["team-away"] = self.fixture.find("span", class_="sp-c-fixture__team--time-away") \
                                                .find("span", class_="qa-full-team-name").text
                        #self.my_fixture["score-home"] = self.fixture.find("span", class_="sp-c-fixture__number--home").text
                        #self.my_fixture["score-away"] = self.fixture.find("span", class_="sp-c-fixture__number--away").text
                        if self.fixture.find("span", class_="sp-c-fixture__status"):
                            self.my_fixture["status"] = self.fixture.find("span", class_="sp-c-fixture__status").text.split(" ",1)[0] + "'"
                        else:
                            self.my_fixture["status"] = ""

                        if self.fixture.find("span", class_="sp-c-fixture__number--time"):
                            self.my_fixture["start-time"] = self.fixture.find("span", class_="sp-c-fixture__number--time").text
                        else:
                            self.my_fixture["start-time"] = ""
                
                        return self.my_fixture
                        
        return self.my_fixture
    def get_all_fixtures(self):
    
        self.LIVESCORE_URL = 'https://www.bbc.co.uk/sport/football/fa-cup/scores-fixtures/'
        
        self.now = datetime.now() # current date and time
        self.url = self.LIVESCORE_URL + self.now.strftime("%Y-%m-%d")
        self.page = urlopen(self.url)
        self.soup = BeautifulSoup(self.page.read(), "lxml")

        self.all_my_fixtures = []

        self.all_fixtures = self.soup.find_all("li", class_="gs-o-list-ui__item gs-u-pb-")  
        if self.all_fixtures:
            for self.fixture in self.all_fixtures:
                my_fixture = {}
                if self.fixture.find("span", class_="sp-c-fixture__team-name--home"):
                    my_fixture["team-home"] = self.fixture.find("span", class_="sp-c-fixture__team-name--home") \
                                            .find("span", class_="qa-full-team-name").text
                    my_fixture["team-away"] = self.fixture.find("span", class_="sp-c-fixture__team-name--away") \
                                            .find("span", class_="qa-full-team-name").text
                    my_fixture["score-home"] = self.fixture.find("span", class_="sp-c-fixture__number--home").text
                    my_fixture["score-away"] = self.fixture.find("span", class_="sp-c-fixture__number--away").text
                    if self.fixture.find("span", class_="sp-c-fixture__status"):
                        my_fixture["status"] = self.fixture.find("span", class_="sp-c-fixture__status").text.replace('Extra Time ', '').split(" ",1)[0]
                        my_fixture["status"] = my_fixture["status"] + ("'" if my_fixture["status"].isnumeric() else "")
                    else:
                        my_fixture["status"] = ""

                    if self.fixture.find("span", class_="sp-c-fixture__number--time"):
                        my_fixture["start-time"] = self.fixture.find("span", class_="sp-c-fixture__number--time").text
                    else:
                        my_fixture["start-time"] = ""
            
                    self.all_my_fixtures.append(my_fixture)
                else: # Not started
                    my_fixture["team-home"] = self.fixture.find("span", class_="sp-c-fixture__team--time-home") \
                                            .find("span", class_="qa-full-team-name").text
                    my_fixture["team-away"] = self.fixture.find("span", class_="sp-c-fixture__team--time-away") \
                                            .find("span", class_="qa-full-team-name").text
                    my_fixture["score-home"] = "0"
                    my_fixture["score-away"] = "0"
                    if self.fixture.find("span", class_="sp-c-fixture__status"):
                        my_fixture["status"] = self.fixture.find("span", class_="sp-c-fixture__status").text.split(" ",1)[0]
                        my_fixture["status"] = my_fixture["status"] + ("'" if my_fixture["status"].isnumeric() else "")
                    else:
                        my_fixture["status"] = ""

                    if self.fixture.find("span", class_="sp-c-fixture__number--time"):
                        my_fixture["start-time"] = self.fixture.find("span", class_="sp-c-fixture__number--time").text
                    else:
                        my_fixture["start-time"] = ""
            
                    self.all_my_fixtures.append(my_fixture)
        return self.all_my_fixtures