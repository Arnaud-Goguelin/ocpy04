from typing import TYPE_CHECKING

from colorama import Fore

from utils import print_title

if TYPE_CHECKING:
    from models.tournament import Tournament


class TournamentListView:
    @staticmethod
    def display_tournaments_list(tournaments: list["Tournament"]):
        print_title("\u265b Tournaments List \u2655 :")

        for tournament in tournaments:
            print(
                f"{Fore.LIGHTYELLOW_EX}{tournaments.index(tournament) + 1}{Fore.RESET}. "
                f"{tournament.name} in {tournament.location}, "
                f"{tournament.start_date if tournament.start_date else "To begin"} - "
                f"{tournament.end_date if tournament.end_date else "Not finished"}."
            )

        input(f"\nPress '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' to go back to Player Menu")
        return None
