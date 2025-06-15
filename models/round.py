from datetime import datetime
from typing import TYPE_CHECKING

from models.match import Match

if TYPE_CHECKING:
    from models.data import Data


class Round:
    """Represents a round in a competition or other event.

    Attributes:
        name (str): A string representing the name of the round.
        matches (set[Match]): A set of Match objects representing the matches in the
            round.
        start_date (datetime | None): A datetime object representing when the round
            started, or None if the round has not started yet.
    """

    def __init__(self, name: str, matches: set[Match], start_date: datetime | None = None):
        self.name: str = name
        self.matches: set[Match] = matches
        self.start_date: datetime | None = start_date

    def start(self):
        """Sets the start_date attribute to the current datetime."""
        self.start_date = datetime.now()

    @property
    def match_count(self) -> int:
        """Returns the number of matches in the round."""
        return len(self.matches)

    @property
    def is_round_finished(self) -> bool:
        """Returns True if all matches in the round have finished, False otherwise."""
        return all(match.is_match_finished for match in self.matches)

    def to_dict(self):
        """Converts the attributes and their values of an instance into a dictionary"""
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
        """Constructs an instance of the class from a dictionary."""
        start_date = datetime.fromisoformat(round_dict["start_date"]) if round_dict["start_date"] else None
        matches = set(Match.from_dict(match_dict, data) for match_dict in round_dict["matches"])
        return cls(
            name=round_dict["name"],
            matches=matches,
            start_date=start_date,
        )
