from typing import TYPE_CHECKING

from colorama import Fore

from utils import (
    CANCELLED_INPUT,
    print_title,
)

if TYPE_CHECKING:
    from models.tournament import Tournament


class TournamentListView:
    @staticmethod
    def display_tournaments_list(tournaments: list["Tournament"]):
        for tournament in tournaments:
            print(
                f"{Fore.LIGHTYELLOW_EX}{tournaments.index(tournament) + 1}{Fore.RESET}. "
                f"{tournament.name} in {tournament.location}, "
                f"{tournament.start_date if tournament.start_date else "To begin"} - "
                f"{tournament.end_date if tournament.end_date else "Not finished"}."
            )

    @classmethod
    def handle_tournaments_list(cls, tournaments: list["Tournament"]):
        print_title("\u265b Tournaments List \u2655 :")

        # TODO: raise value error stop app, handle it in controller
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
