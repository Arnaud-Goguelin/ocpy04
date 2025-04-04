import datetime
import random

from models.match import Match
from models.player import Player
from models.round import Round
from utils import MAX_NUMBER_OF_ROUNDS


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
        self.past_players_paires = set()
        # technical specifications recommend that a tournament also has:
        # a max rounds number, a current round number.
        # YET max rounds number is a constant common to all Tournament, thus it is stored in constants.py file
        # current round number can be return with a method, no need to store it

    def get_player_scores(self):
        """
        Calculate and return the total scores for each player across all rounds and matches in current tournament.
        """
        player_scores = {player: 0 for player in self.players}

        # when tournament start, no player has a score
        if not self.rounds:
            return player_scores

        for round in self.rounds:
            for match in round.matches:
                player_scores[match.player1] += match.score_player1
                player_scores[match.player2] += match.score_player2
        return player_scores

    def rank_players(self):
        """
        Sort players by their scores in ascending order in current tournament.
        """
        player_scores = self.get_player_scores()
        sorted_players = sorted(player_scores, key=player_scores.get, reverse=False)
        return sorted_players

    def have_played(self, player1: Player, player2: Player):
        # for round in self.rounds:
        #     for match in round.matches:
        #         if (player1 == match.player1 and player2 == match.player2) or (
        #                 player1 == match.player2 and player2 == match.player1):
        #             return True
        # return False
        return (player1, player2) in self.past_players_paires or (player2, player1) in self.past_players_paires

    def create_matches(self):
        """
        Create matches by generating pairs of players from the list of players of current tournament.
        """
        matches = []
        players_for_pairing = []
        if not self.rounds:
            # as we work with instance attribute, no need to shuffle a copy,
            # it will only modify this instance attribute
            random.shuffle(self.players)
            players_for_pairing = self.players
        else:
            players_for_pairing = self.rank_players()

        # create pairs of players to create Match,
        # [::2] select element with even index, [1::2] select element with odd index
        # reminder: [start:stop:step] => https://stackoverflow.com/questions/509211/how-slicing-in-python-works
        paires_to_dispatch = [zip(players_for_pairing[::2], players_for_pairing[1::2])]

        for odd_player, even_player in paires_to_dispatch:
            # instead of storing players paires in have_played attributes,
            # we could simply iterate rounds and then matches
            # to know which players have already played together and store the paires un a list.
            # Yet this would be an algorithm with linear complexity
            # Nevertheless, have_played attributes do not respect DB standardization
            have_played = self.have_played(odd_player, even_player)
            if not have_played:
                match = Match(odd_player, even_player)
                matches.append(match)
                self.past_players_paires.add((odd_player, even_player))
                paires_to_dispatch.pop(0)
            else:
                # identify first and second paires, first one is an invalid one which didn't pass previous test
                invalid_first_paire = paires_to_dispatch[0]
                second_paire = paires_to_dispatch[1]
                # delete them
                paires_to_dispatch.pop(0)
                paires_to_dispatch.pop(1)
                # insert at the same place different paires of players
                paires_to_dispatch.insert(0, (invalid_first_paire[0], second_paire[0]))
                paires_to_dispatch.insert(1, (invalid_first_paire[1], second_paire[1]))

        return matches

    # a property allow us to call a method as an attribute and not as a function
    # cache_property also exist to store value in a cache in instance
    @property
    def rounds_count(self):
        """
        Return rounds attribute length, thus the current round number in current tournament.
        """
        return len(self.rounds)

    def create_round(self, matches: list[Match]):
        """
        Creates a new tournament round, initializes it, and appends it to the list of
        existing rounds in current tournament.
        """
        new_round = Round(
            name=f"Round {self.rounds_count + 1}",
            matches=matches,
        )
        new_round.start()
        self.rounds.append(new_round)
        return None

    def start(self):
        """
        Starts the process by initializing the start date, shuffling players, and creating rounds.
        """
        self.start_date = datetime.datetime.now()

        # --- create and start rounds ---
        # range stop at MAX_NUMBER_OF_ROUNDS -1, so we begin at 0 to have 4 iteration anyway
        for i in range(0, MAX_NUMBER_OF_ROUNDS):
            matches = self.create_matches()
            self.create_round(matches)
