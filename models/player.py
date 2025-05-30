from datetime import datetime


class Player:

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: str,
        chess_id: str,
        chess_ids_from_data: list[str] = None,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name.upper()
        self.birthdate = self.validate_birth_date(birthdate)
        self.chess_id = self.validate_chess_is(chess_id, chess_ids_from_data)

    @staticmethod
    def validate_chess_is(chess_id: str, chess_ids_from_data: list[str] = None) -> str:
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
    def validate_birth_date(birthdate: str) -> str:
        """
        Validates birthdate to respect format: DD-MM-YYYY.
        Raises ValueError if not.
        """
        try:
            datetime.strptime(birthdate, "%d-%m-%Y")
            return birthdate
        except ValueError:
            raise ValueError("Birth date must be in DD-MM-YYYY format with only digits.")

    def to_dict(self):
        player_dict = {}

        for key, value in self.__dict__.items():
            if not callable(value) and not isinstance(value, (classmethod, staticmethod, property)):
                player_dict[key] = value

        return player_dict
