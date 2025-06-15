from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .data import Data


class Player:
    """
    Represents a chess player with information such as name, birthdate, and chess ID.

    Attributes:
        first_name (str): The first name of the player.
        last_name (str): The last name of the player, stored in uppercase.
        birthdate (str): The validated birthdate of the player in "DD-MM-YYYY" format.
        chess_id (str): A unique and validated chess ID, following a format of two
            uppercase letters followed by five digits.
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: str,
        chess_id: str,
        chess_ids_from_data: list[str] = None,
    ) -> None:
        self.first_name: str = self.__validate_name(first_name)
        self.last_name: str = self.__validate_name(last_name.upper())
        self.birthdate: str = self.__validate_birth_date(birthdate)
        self.chess_id: str = self.__validate_chess_is(chess_id, chess_ids_from_data)

    @staticmethod
    def __validate_chess_is(chess_id: str, chess_ids_from_data: list[str] = None) -> str:
        """
        Validates and formats a chess ID.
        Ensure it has 7 characters long, begins with 2 capital letters, and ends with 5 digits.
        Raise ValueError if not.
        """
        characters = [*chess_id]

        if chess_ids_from_data and chess_id in chess_ids_from_data:
            raise ValueError("Chess ID already used.")

        if len(characters) != 7:
            raise ValueError("Chess ID must be 7 characters long: 2 letters + 5 digits.")

        first_two_characters = characters[:2]
        does_chess_id_begins_with_letters = all(character.isalpha() for character in first_two_characters)
        if not does_chess_id_begins_with_letters:
            raise ValueError("Chess ID must begins with 2 letters.")

        five_last_characters = characters[-5:]
        does_chess_id_ends_with_digits = all(character.isdigit() for character in five_last_characters)
        if not does_chess_id_ends_with_digits:
            raise ValueError("Chess ID must end with 5 digits.")

        upper_characters = [character.upper() for character in first_two_characters]
        valide_chess_id = "".join((upper_characters + five_last_characters))

        return valide_chess_id

    @staticmethod
    def __validate_birth_date(birthdate: str) -> str:
        """
        Validates birthdate to respect format: DD-MM-YYYY.
        Raises ValueError if not.
        """
        try:
            parsed_date = datetime.strptime(birthdate, "%d-%m-%Y")

        except ValueError:
            raise ValueError("Birth date must be in DD-MM-YYYY format with only digits.")
        if parsed_date.year < datetime(year=1900, month=1, day=1).year:
            raise ValueError("Player birth date must be after 1900.")
        if parsed_date > datetime.now():
            raise ValueError("Player birth date must be before today.")
        return birthdate

    @staticmethod
    def __validate_name(name: str) -> str:
        """Validates that a given name is a non-empty string."""
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if name.isdigit():
            raise ValueError("Name cannot be a number")
        if not name.strip():
            raise ValueError("Name cannot be empty")
        return name

    def to_dict(self):
        """
        Converts the attributes of the object to a dictionary representation.
        """
        player_dict = {}

        for key, value in self.__dict__.items():
            if not callable(value) and not isinstance(value, (classmethod, staticmethod, property)):
                player_dict[key] = value

        return player_dict

    @classmethod
    # in Data.load() we call from_dict for Player and Tournament classes
    # Tournament need data but not Player, thus we need to pass data as argument
    # and set e default value to None to ignore it in Player.from_dict() method
    def from_dict(cls, player_dict, data=None):
        """
        Constructs an instance of the class from a dictionary.
        """
        return cls(**player_dict)

    @classmethod
    def get_player_from_id(cls, chess_id: str, data: "Data") -> "Player":
        """
        Retrieves a Player instance from the dataset based on the provided chess ID.
        Args:
            chess_id: The chess ID used to identify the player in the dataset.
            data: The Data object that contains the list of Player instances.

        Returns:
            Player: The Player instance corresponding to the provided chess ID.

        Raises:
            ValueError: If no player with the provided chess ID is found in the dataset.
        """
        valide_chess_id = cls.__validate_chess_is(chess_id)
        try:
            return next(player for player in data.players if player.chess_id == valide_chess_id)
        except StopIteration:
            raise ValueError(f"Player with {valide_chess_id} not found.")
