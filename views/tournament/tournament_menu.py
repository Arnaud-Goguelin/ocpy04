from colorama import Fore

from utils import CANCELLED_INPUT, print_title


class TournamentMenuView:

    @staticmethod
    def display():
        print_title("\u265e  Tournament Menu \u2658 :")

        print(f"{Fore.LIGHTYELLOW_EX}1{Fore.RESET}. Create new tournament \u265b.")
        print(f"{Fore.LIGHTYELLOW_EX}2{Fore.RESET}. View tournament details \u265c.")
        print(f"{Fore.LIGHTYELLOW_EX}3{Fore.RESET}. Start or continue tournament \u265e.")
        print(
            f"\u265f\u2659 Press "
            f"'{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}' to return to Main menu "
            f"\u2659\u265f."
        )

        return input(f"{Fore.LIGHTYELLOW_EX}Choose an option : {Fore.RESET}")
