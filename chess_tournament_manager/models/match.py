from typing import TYPE_CHECKING

from .player import Player

if TYPE_CHECKING:
    from .data import Data


class Match:
    """
    Represents a match between two players in a competitive context.

    Attributes:
        player1 (Player): The first player participating in the match.
        player2 (Player): The second player participating in the match.
        score_player1 (float): The score of the first player, initialized to 0 by default.
        score_player2 (float): The score of the second player, initialized to 0 by default.
    """

    def __init__(self, player1: Player, player2: Player, score_player1: float = 0, score_player2: float = 0):
        self.player1: Player = player1
        self.player2: Player = player2
        self.score_player1: float = score_player1
        self.score_player2: float = score_player2

    def player1_wins(self) -> None:
        """
        Increments the score of Player 1 by 1 while keeping Player 2's score unchanged.
        """
        self.score_player1 += 1
        self.score_player2 += 0
        return None

    def player2_wins(self) -> Player:
        """
        Increments the score of Player 2 by 1 while keeping Player 1's score unchanged.
        """
        self.score_player1 += 0
        self.score_player2 += 1
        return None

    def draw(self) -> None:
        """
        Updates the current score of both players by 0.5 to reflect a draw scenario.
        """
        self.score_player1 += 0.5
        self.score_player2 += 0.5
        return None

    @property
    def is_match_finished(self) -> bool:
        """
        Checks if the match has finished.
        Returns:
            bool: True if the match is finished, False otherwise.
        """
        return self.score_player1 != 0 or self.score_player2 != 0

    @property
    def participating_players(self) -> list[Player]:
        """
        Returns a list of players participating in the current game.
        """
        return [self.player1, self.player2]

    def to_dict(self):
        """
        Converts the attributes and their values of an instance into a dictionary
        representation.
        """
        match_dict = {}

        for key, value in self.__dict__.items():
            if not callable(value) and not isinstance(value, (classmethod, staticmethod, property)):
                # Players instances are already stored in another file and can exist without tournaments
                # So it is not relevant to store them again with tournaments
                if key == "player1" or key == "player2":
                    match_dict[key] = value.chess_id
                else:
                    match_dict[key] = value

        return match_dict

    @classmethod
    def from_dict(cls, match_dict, data: "Data"):
        """
        Constructs an instance of the class from a dictionary.
        """
        return cls(
            player1=Player.get_player_from_id(match_dict["player1"], data),
            player2=Player.get_player_from_id(match_dict["player2"], data),
            score_player1=match_dict["score_player1"],
            score_player2=match_dict["score_player2"],
        )
