from models.player import Player


class Match:
    def __init__(self, player1: Player, player2: Player, score_player1: float = 0, score_player2: float = 0):
        self.player1: Player = player1
        self.player2: Player = player2
        self.score_player1: float = score_player1
        self.score_player2: float = score_player2

    def player1_wins(self) -> None:
        self.score_player1 += 1
        self.score_player2 += 0
        return None

    def player2_wins(self) -> Player:
        self.score_player1 += 0
        self.score_player2 += 1
        return None

    def draw(self) -> None:
        self.score_player1 += 0.5
        self.score_player2 += 0.5
        return None

    @property
    def is_match_finished(self) -> bool:
        return self.score_player1 != 0 or self.score_player2 != 0

    @property
    def participating_players(self) -> list[Player]:
        return [self.player1, self.player2]

    def to_dict(self):
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
    def from_dict(cls, match_dict):
        return cls(**match_dict)
