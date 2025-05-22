from colorama import Fore

from utils import CANCELLED_INPUT, print_title


class MainMenuView:

    @staticmethod
    def display():
        print_title("\u265a  Welcome to the Chess Tournament Manager \u2654 :")

        print(f"{Fore.LIGHTYELLOW_EX}1. {Fore.RESET}Manage Players \u265d.")
        print(f"{Fore.LIGHTYELLOW_EX}2. {Fore.RESET}Manage Tournaments \u265e.")
        print(
            f"\u265f\u2659 "
            f"Press '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}' to exit and close application "
            f"\u2659\u265f."
        )

        choice =  input(f"{Fore.LIGHTYELLOW_EX}Choose an option : {Fore.RESET}")
        if isinstance(choice, str) :
            choice = choice.upper()
        return choice