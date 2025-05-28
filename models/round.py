import datetime
from typing import TYPE_CHECKING

from models.match import Match

if TYPE_CHECKING:
    pass


class Round:

    def __init__(self, name: str, matches: list[Match]):
        self.name = name
        self.matches = matches
        self.start_date = None

    def start(self):
        self.start_date = datetime.datetime.now()

    @property
    def match_count(self) -> int:
        return len(self.matches)

    @property
    def is_round_finished(self) -> bool:
        return all(match.is_match_finished for match in self.matches)
