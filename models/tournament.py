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
        return (player1, player2) in self.past_players_paires or (player2, player1) in self.past_players_paires
        # for round in self.rounds:
        #     for match in round.matches:
        #         if (player1 == match.player1 and player2 == match.player2) or (
        #                 player1 == match.player2 and player2 == match.player1):
        #             return True
        # return False

    def create_matches(self):
        """
        Create matches by generating pairs of players from the list of players of current tournament.
        """
        matches = []
        available_players = []
        if not self.rounds:
            # as we work with instance attribute, no need to shuffle a copy,
            # it will only modify this instance attribute
            random.shuffle(self.players)
            # /!\ yet store a copy in available_players as after we will remove player from it,
            # just use available_players as a reference would remove players from self.players
            # and bugs will happen in round 2
            available_players = self.players.copy()
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
                # that mean current_player have already played with every other
                # yet we still need a match, thus we create a match with current_player
                # (already out of the list of available_players)
                # with first next player thus available_players[0] which we also remove from the list thanks to pop()
                possible_opponent = available_players.pop(0)
                match = Match(current_player, possible_opponent)
                matches.append(match)
                self.past_players_paires.add((current_player, possible_opponent))

        return matches

    # a property allow us to call a method as an attribute and not as a function
    # cache_property also exist to store value in a cache in instance
    @property
    def rounds_count(self):
        """
        Return rounds attribute length, thus the current round number in current tournament.
        """
        return len(self.rounds)

    @property
    def rounds_matches_count(self):
        """
        Return rounds attribute length, thus the current round number in current tournament.
        """
        matches_count = 0
        for round in self.rounds:
            matches_count += len(round.matches)

        return print(f"rounds = {len(self.rounds)}, matches = {matches_count}")

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
            if matches:
                self.create_round(matches)
            else:
                break
