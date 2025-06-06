from datetime import datetime
from typing import TYPE_CHECKING

from models.match import Match

if TYPE_CHECKING:
    from models.data import Data


class Round:

    def __init__(self, name: str, matches: set[Match], start_date: datetime | None = None):
        self.name: str = name
        self.matches: set[Match] = matches
        self.start_date: datetime | None = start_date

    def start(self):
        self.start_date = datetime.now()

    @property
    def match_count(self) -> int:
        return len(self.matches)

    @property
    def is_round_finished(self) -> bool:
        return all(match.is_match_finished for match in self.matches)

    def to_dict(self):
        round_dict = {}

        for key, value in self.__dict__.items():
            if not callable(value) and not isinstance(value, (classmethod, staticmethod, property)):
                if key == "matches":
                    round_dict[key] = [match.to_dict() for match in value] if value else []
                elif key == "start_date":
                    round_dict[key] = value.isoformat() if value else None
                else:
                    round_dict[key] = value

        return round_dict

    @classmethod
    def from_dict(cls, round_dict, data: "Data"):
        start_date = datetime.fromisoformat(round_dict["start_date"]) if round_dict["start_date"] else None
        matches = set(Match.from_dict(match_dict, data) for match_dict in round_dict["matches"])
        return cls(
            name=round_dict["name"],
            matches=matches,
            start_date=start_date,
        )
