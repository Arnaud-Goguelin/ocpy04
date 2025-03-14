import datetime


class Tournament:

    def __init__(self, name: str, location: str, description: str, players: list[Player]):
        self.name = name
        self.location = location
        self.description = description
        self.players = players
        self.start_date = None
        self.end_date = None
        self.rounds = []
        #TODO : scores?

    def start(self):
        self.start_date = datetime.datetime.now()
        # shuffle players
        # create matches instances
        # create a first round instance
        # add matches to round
        # add round to self.rounds from this tournament instance

    # a property allow us to call a method as an attribute and not as a function
    # print(tournament.rounds_count) will return 
    @property
    def rounds_count(self):
        return len(self.rounds)