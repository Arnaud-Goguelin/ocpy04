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

    def player2_wins(self) -> None:
        self.score_player1 += 0
        self.score_player2 += 1
        return None

    def drown(self)-> None:
        self.score_player1 += 0.5
        self.score_player2 += 0.5
        return None

    def set_match_score(self, winner: Player | None = None) -> None:

        if winner != self.player1 and winner != self.player2:
            raise ValueError(f"Player {winner.last_name} did not play this match.")

        result_actions = {
            self.player1: self.player1_wins,
            self.player2: self.player2_wins,
            }

        action = result_actions.get(winner, self.drown)
        action()
        return None

    @property
    def is_match_finished(self) -> bool:
        return self.score_player1 != 0 and self.score_player2 != 0

    @property
    def participating_players(self) -> list[Player]:
        return [self.player1, self.player2]


