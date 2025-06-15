from chess_tournament_manager.utils import print_title


class CreateTournamentView:
    """A class representing the view for creating a new tournament."""

    @staticmethod
    def display_add_tournament_form():
        """Displays the form to add a new tournament."""
        print_title("\u265b  Create a new Tournament   \u2655 :")

        name = input("Tournament's name : ")
        location = input("Location : ")
        description = input("Description : ")

        return name, location, description
