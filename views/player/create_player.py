from utils import print_title


class CreatePlayerView:
    """A class representing the view for creating a new player."""

    @staticmethod
    def display_add_player_form():
        """Displays the form to add a new player."""
        print_title("\u265d  Add New Player   \u2657 :")

        first_name = input("First name : ")
        last_name = input("Last Name : ")
        birthdate = input("Birthdate (DD-MM-YYYY) : ")
        chess_id = input("Chess ID (2 letters + 5 digits) : ")
        return first_name, last_name, birthdate, chess_id
