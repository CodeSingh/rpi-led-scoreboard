from livescores import *

class LivescoreManager:

    def __init__(self):
        pass

    def get_competitions(self): 
        competitions = []
        for cls in livescore.Livescore.__subclasses__():
            competitions.append({"ID" : cls.ID, "Name" : cls.NAME})
        return competitions

    
    def get_live_score_class(self, livescore_id, team):
        for cls in livescore.Livescore.__subclasses__():
            if cls.ID == livescore_id:
                return cls(team)
        raise ValueError