from typing import TYPE_CHECKING

from colorama import Fore

from chess_tournament_manager.utils import (
    CANCELLED_INPUT,
    print_title,
)

if TYPE_CHECKING:
    from chess_tournament_manager.models.tournament import Tournament


class TournamentListView:
    """
    Represents a view for displaying and interacting with a list of tournaments.
    """

    @staticmethod
    def display_tournaments_list(tournaments: list["Tournament"]):
        """
        Displays a list of tournaments with their details.

        Args:
            tournaments (list[Tournament]): A list containing instances of the `Tournament`
                class, which represent tournaments to be displayed.
        """
        for tournament in tournaments:
            print(
                f"{Fore.LIGHTYELLOW_EX}{tournaments.index(tournament) + 1}{Fore.RESET}. "
                f"{tournament.name} in {tournament.location}, "
                f"{tournament.start_date if tournament.start_date else "To begin"} - "
                f"{tournament.end_date if tournament.end_date else "Not finished"}."
            )

    @classmethod
    def handle_tournaments_list(cls, tournaments: list["Tournament"]):
        """
        Handles the display and selection process for a list of tournaments. The method prompts
        the user to select a tournament or return to the tournament menu without saving.

        Args:
            tournaments (list[Tournament]): A list of Tournament objects to be displayed and
                selected from.

        Raises:
            ValueError: If the input list of tournaments is empty.

        Returns:
            str: The user's choice, representing the selected tournament index or the indicator
                to return to the tournament menu without saving.
        """
        print_title("\u265b Tournaments List \u2655 :")

        if not tournaments:
            raise ValueError("No tournaments to display.")

        print(f"{Fore.LIGHTYELLOW_EX}---{Fore.RESET} Please select a tournament. {Fore.LIGHTYELLOW_EX}---{Fore.RESET}")
        cls.display_tournaments_list(tournaments)

        choice = input(
            f"\n{Fore.LIGHTYELLOW_EX}What would you like to do?{Fore.RESET}"
            f"\nSelect a tournament: {Fore.LIGHTYELLOW_EX}copy index{Fore.RESET} / "
            f"Go back to Tournament Menu without saving, press '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}'\n:"
        )

        return choice
