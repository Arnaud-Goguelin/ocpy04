import datetime

from models.match import Match


class Round:

    def __init__(self, name: str, matches: list[Match]):
        self.name = name
        self.matches = matches
        self.start_date = None

    def start(self):
        self.start_date = datetime.datetime.now()
        for match in self.matches:
            match.start()
