import datetime

class Player:

    def __init__(self, first_name: str, last_name: str, birthday: str, chess_id: str ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.chess_id = self.validate_chess_is(chess_id)

    @staticmethod
    def validate_chess_is( chess_id : str) -> str:
        characters = [*chess_id]

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
        valide_chess_id = ''.join((upper_characters + five_last_characters))

        return valide_chess_id

