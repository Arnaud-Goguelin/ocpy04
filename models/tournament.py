import datetime
import random

from models.match import Match
from models.player import Player
from models.round import Round
from utils import MAX_NUMBER_OF_ROUNDS


class Tournament:

    def __init__(self, name: str, location: str, description: str, players: set[Player]) -> None:
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
        # YET max rounds number is a constant common to all Tournaments, thus it is stored in constants.py file
        # current round number can be returned with a method, no need to store it

    @staticmethod
    def validate_players(players: set[Player]) -> None:

        if len(players) % 2 != 0:
            raise ValueError("Tournament must have an even number of players")
        # 'for' loop is less effective but allow a preciser error message
        for player in players:
            if not isinstance(player, Player):
                raise ValueError(f"{player} must be registered as a Player before participating in a tournament")
        return None

    # a property allows us to call a method as an attribute and not as a function
    # cache_property also exist to store value in a cache in instance
    @property
    def rounds_count(self):
        """
        Return rounds attribute length, thus the current round number in the current tournament.
        """
        return len(self.rounds)

    def get_player_scores(self):
        """
        Calculate and return the total scores for each player across all rounds and matches in the current tournament.
        """
        player_scores = {player: 0 for player in self.players}
        # when tournament start, no player has a score
        if not self.rounds:
            return player_scores

        for tournament_round in self.rounds:
            for match in tournament_round.matches:
                player_scores[match.player1] += match.score_player1
                player_scores[match.player2] += match.score_player2

        return player_scores

    def rank_players(self):
        """
        Sort players by their scores in ascending order in the current tournament.
        """
        player_scores = self.get_player_scores()
        sorted_players = sorted(player_scores, key=player_scores.get, reverse=False)
        return sorted_players

    def have_played(self, player1: Player, player2: Player):
        return (player1, player2) in self.past_players_paires or (player2, player1) in self.past_players_paires

    def create_matches(self):
        """
        Create matches by generating pairs of players from the list of players of the current tournament.
        """
        matches = []
        if not self.rounds:

            players_list = list(self.players)
            random.shuffle(players_list)
            # as we convert the set() to a list, we do not need to store a copy in available_players variable
            # later in code we might remove player from list, but it won't alter set in players attributes
            available_players = players_list

        else:
            available_players = self.rank_players()

        while available_players:
            current_player = available_players.pop(0)
            for possible_opponent in available_players:
                if not self.have_played(current_player, possible_opponent):
                    match = Match(current_player, possible_opponent)
                    matches.append(match)
                    self.past_players_paires.add((current_player, possible_opponent))
                    available_players.remove(possible_opponent)
                    break
            else:
                # if instruction 'for' end without breaking,
                # that mean current_player have already played with every other,
                # yet we still need a match, thus we create a match with current_player
                # (already out of the list of available_players)
                # with the first next player thus available_players[0]
                # which we also remove from the list thanks to pop()
                possible_opponent = available_players.pop(0)
                match = Match(current_player, possible_opponent)
                matches.append(match)
                self.past_players_paires.add((current_player, possible_opponent))

        return matches

    def create_round(self, matches: list[Match]):
        """
        Creates a new tournament round, initializes it, and appends it to the list of
        existing rounds in the current tournament.
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
        Starts the process by initializing the start date, shuffling players, and creating the first round.
        """
        self.start_date = datetime.datetime.now()
        matches = self.create_matches()
        if matches:
            self.create_round(matches)
        return None

    def continue_tournament(self):

        max_possible_rounds = (len(self.players) * (len(self.players) - 1)) / 2

        if self.rounds_count < min(MAX_NUMBER_OF_ROUNDS, max_possible_rounds):
            matches = self.create_matches()
            if matches:
                self.create_round(matches)

        return None

    def end(self):
        self.end_date = datetime.datetime.now()
