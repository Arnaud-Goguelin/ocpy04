import datetime
import random

from models.match import Match
from models.player import Player
from models.round import Round


class Tournament:

    def __init__(self, name: str, location: str, description: str, players: list[Player]) -> None:
        if len(players) % 2 != 0:
            raise ValueError("Tournament must have an even number of players")

        self.name = name
        self.location = location
        self.description = description
        self.players = players
        self.start_date = None
        self.end_date = None
        self.rounds = []
        # technical specifications recommend that a tournament also has:
        # a max rounds number, a current round number.
        # YET max rounds number is a constant common to all Tournament, thus it is stored in constants.py file
        # current round number can be return with a method, no need to store it

    def start(self):
        self.start_date = datetime.datetime.now()

        print("self.players = ")
        for player in self.players:
            print(player.first_name)
        # --- shuffle players ---
        # as we work with instance attribute, no need to shuffle a copy, it will only modify this instance attribute
        random.shuffle(self.players)
        print("self.players shuffled = ")
        for player in self.players:
            print(player.first_name)

        # --- create matches ---
        # create pairs of players to create Match, [::2] select element with even index, [1::2] select element with odd index
        # reminder: [start:stop:step] => https://stackoverflow.com/questions/509211/how-slicing-in-python-works
        matches = []

        print("zip = ")
        for player1, player2 in zip(self.players[::2], self.players[1::2]):
            print(player1.first_name, player2.first_name)
            match = Match(player1, player2)
            print(match.__dict__)
            matches.append(match)

        # --- create round ---
        print("matches = ", len(matches))
        round1 = Round(name="Round 1", matches=matches)
        round1.start()  # ?? start round here?
        self.rounds.append(round1)

    # create method next round

    # create a method to iterate in rounds and interates in match to get score by player

    # create a method to avoid a match already done in 2 players

    # a property allow us to call a method as an attribute and not as a function
    # cache_property also exist to store value in a cache in instance
    @property
    def rounds_count(self):
        """
        Return rounds attribute length, thus the current round number.
        """
        return len(self.rounds)
