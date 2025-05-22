from typing import TYPE_CHECKING

from colorama import Fore

from utils import (
    CANCELLED_INPUT,
    print_title,
    )

if TYPE_CHECKING:
    from models.tournament import Tournament


# TODO: should a view handle inputs???
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

        if not tournaments:
            raise ValueError("No tournaments to display.")

        # if is_used_for_selecting_tournaments is False:
        #     cls.display_tournaments_list(tournaments)
        #     input(f"\nPress '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' to go back to Player Menu")
        #     return None

        print("Please select a tournament to start or to continue.")
        cls.display_tournaments_list(tournaments)

        choice = input(
            f"\n{Fore.LIGHTYELLOW_EX}What would you like to do?{Fore.RESET}"
            f"\nSelect a tournament: {Fore.LIGHTYELLOW_EX}copy index{Fore.RESET} / "
            f"Go back to Tournament Menu without saving, press '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}'\n:"
        )

        if choice.upper() == CANCELLED_INPUT:
            return None

        elif not choice.isdigit():
            print(
                f"\n{Fore.RED}Invalid index. Please enter a valid player's index or press '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' or '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}' to exit the menu.{Fore.RESET}"
            )
        else:
            tournament_index = int(choice) - 1

            if not 0 <= tournament_index < len(tournaments):
                print(
                    f"\n{Fore.RED}Invalid index. Please enter a valid player's index or press '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' or '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}' to exit the menu.{Fore.RESET}"
                )
            else:
                return tournaments[tournament_index]
