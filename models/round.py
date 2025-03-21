from models.match import Match
import datetime

class Round:

    def __init__(self, name: str, matches: list[Match]):
        self.name = name
        self.matches = matches
        self.start_date = None

    def start(self):
        self.start_date = datetime.datetime.now()
