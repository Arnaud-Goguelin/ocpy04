import random
from datetime import datetime
from typing import TYPE_CHECKING

from .match import Match
from .player import Player
from .round import Round
from ..utils import MAX_NUMBER_OF_ROUNDS, create_id

if TYPE_CHECKING:
    from .data import Data


class Tournament:
    """
    Represents a tournament consisting of players, rounds, and matches. Manages the logic
    to validate players, organize matches, proceed with rounds, calculate player scores, and
    handle tournament progression.

    Attributes:
        id (str): Unique identifier of the tournament.
        name (str): Name of the tournament.
        location (str): Location where the tournament is held.
        description (str): Detailed description of the tournament.
        players (set[Player]): Set of players participating in the tournament.
        start_date (datetime | None): Start date and time of the tournament.
        end_date (datetime | None): End date and time of the tournament.
        rounds (set[Round]): Set of tournament rounds.
        past_players_paires (set[tuple[Player, Player]]):
        Tracks pairs of players that have already played together in matches.
    """

    def __init__(
        self,
        name: str,
        location: str,
        description: str,
        players: set[Player],
        id: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        rounds: set[Round] = None,
        past_players_paires: set[tuple[Player, Player]] = None,
    ) -> None:
        self.id: str = id if id else create_id()
        self.name: str = name
        self.location: str = location
        self.description: str = description
        self.players: set[Player] = players
        self.start_date: datetime | None = start_date
        self.end_date: datetime | None = end_date
        # TODO: just use a list
        self.rounds: set[Round] = rounds
        self.past_players_paires: set[tuple[Player, Player]] = past_players_paires
        # technical specifications recommend that a tournament also has:
        # a max rounds number, a current round number.
        # YET max rounds number is a constant common to all Tournaments, thus it is stored in constants.py file
        # current round number can be returned with a method, no need to store it

    @staticmethod
    def validate_players(players: set[Player]) -> None:
        """
        Validates players for participation in a tournament.

        Ensures the players meet the requirements to participate in a tournament.
        Checks that the number of players is even and that each participant is an
        instance of the Player class.

        Args:
            players (set[Player]): A set of players to validate.

        Raises:
            ValueError: If the number of players is not even.
            ValueError: If any participant is not an instance of the Player class.

        Returns:
            None
        """

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

    @property
    def get_last_round(self):
        """
        Return the last round in the current tournament, according to the start_date of each round.
        """
        if not self.rounds:
            return None

        rounds_with_date = [r for r in self.rounds if r.start_date]
        if not rounds_with_date:
            return None

        return max(rounds_with_date, key=lambda r: r.start_date)

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
        """
        Checks if the two players have already played against each other.
        """
        return (player1, player2) in self.past_players_paires or (player2, player1) in self.past_players_paires

    def create_matches(self):
        """
        Create matches by generating pairs of players from the list of players of the current tournament.
        """
        matches = set()
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
                    matches.add(match)
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
                matches.add(match)
                self.past_players_paires.add((current_player, possible_opponent))

        return matches

    def create_round(self, matches: set[Match]):
        """
        Creates a new tournament round, initializes it, and appends it to the list of
        existing rounds in the current tournament.
        """
        new_round = Round(
            name=f"Round {self.rounds_count + 1}",
            matches=matches,
        )
        new_round.start()
        self.rounds.add(new_round)
        return None

    def start(self):
        """
        Starts the process by initializing the start date, shuffling players, and creating the first round.
        """
        self.start_date = datetime.now()
        matches = self.create_matches()
        if matches:
            self.create_round(matches)
        return None

    def continue_tournament(self):
        """
        Controls the continuation of a tournament by creating rounds and matches based on the
        current state of the tournament and predefined conditions.

        Args:
            self: Instance of the class containing the tournament data, including players,
                rounds played, and methods for creating matches and rounds.

        Returns:
            None: This method does not return a value.
        """

        max_possible_rounds = (len(self.players) * (len(self.players) - 1)) / 2

        if self.rounds_count < min(MAX_NUMBER_OF_ROUNDS, max_possible_rounds):
            matches = self.create_matches()
            if matches:
                self.create_round(matches)

        return None

    def end(self):
        """
        Marks the end of a process or event by setting the end_date attribute
        to the current date and time.
        """
        self.end_date = datetime.now()

    def to_dict(self):
        """
        Converts the instance attributes of the object to a dictionary.
        """
        # TODO: no error handling?
        # TODO: simplify, global logic won't works, it is easier to copy key
        tournament_dict = {}
        for key, value in self.__dict__.items():

            if not callable(value) and not isinstance(value, (classmethod, staticmethod, property)):

                if key == "players":
                    # Players instances are already stored in another file and can exist without tournaments
                    # So it is not relevant to store them again with tournaments
                    tournament_dict[key] = [player.chess_id for player in value]

                elif key == "rounds":
                    # Match are also stored as dict, cf. Round model
                    tournament_dict[key] = [round.to_dict() for round in value] if value else []

                elif key == "past_players_paires":
                    tournament_dict[key] = (
                        [(player1.chess_id, player2.chess_id) for player1, player2 in value] if value else []
                    )
                # TODO: check if there is a way like in Pydantic to define a method to serialize datetime object?
                elif key == "start_date" or key == "end_date":
                    tournament_dict[key] = value.isoformat() if value else None

                else:
                    tournament_dict[key] = value if value else None

        return tournament_dict

    @classmethod
    def from_dict(cls, tournament_dict, data: "Data"):
        """
        Creates a new instance of the class from a dictionary representation of a
        tournament and supplemental data.

        Args:
            tournament_dict: A dictionary containing tournament details such as ID,
                name, location, description, players, rounds, start_date, end_date,
                and past player pairings.
            data (Data): Supplemental data used for resolving player and round details,
                among other information.

        Returns:
            An instance of the class representing the tournament with all provided
            attributes and relationships properly set.
        """
        players = set(Player.get_player_from_id(chess_id, data) for chess_id in tournament_dict["players"])
        rounds = set(Round.from_dict(round_dict, data) for round_dict in tournament_dict["rounds"])
        start_date = datetime.fromisoformat(tournament_dict["start_date"]) if tournament_dict["start_date"] else None
        end_date = datetime.fromisoformat(tournament_dict["end_date"]) if tournament_dict["end_date"] else None
        past_players_paires = set(
            (Player.get_player_from_id(player1_id, data), Player.get_player_from_id(player2_id, data))
            for player1_id, player2_id in tournament_dict["past_players_paires"]
        )

        tournament = cls(
            id=tournament_dict["id"],
            name=tournament_dict["name"],
            location=tournament_dict["location"],
            description=tournament_dict["description"],
            players=players,
            start_date=start_date,
            end_date=end_date,
            rounds=rounds,
            past_players_paires=past_players_paires,
        )

        return tournament
