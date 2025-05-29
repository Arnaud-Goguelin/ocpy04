from models.player import Player


class Match:
    def __init__(self, player1: Player, player2: Player, score_player1: float = 0, score_player2: float = 0):
        self.player1 = player1
        self.player2 = player2
        self.score_player1 = score_player1
        self.score_player2 = score_player2

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
