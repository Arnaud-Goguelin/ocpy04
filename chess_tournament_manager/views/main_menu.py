from colorama import Fore

from ..utils import CANCELLED_INPUT, print_title


class MainMenuView:
    """
    Represents the main menu view for the Chess Tournament Manager application.
    """

    @staticmethod
    def display():
        """
        Displays the main menu of the Chess Tournament Manager application.
        Returns:
            str: The user's input representing their choice from the menu.
        """
        print_title("\u265a  Welcome to the Chess Tournament Manager \u2654 :")

        print(f"{Fore.LIGHTYELLOW_EX}1. {Fore.RESET}Manage Players \u265d.")
        print(f"{Fore.LIGHTYELLOW_EX}2. {Fore.RESET}Manage Tournaments \u265e.")
        print(f"{Fore.LIGHTYELLOW_EX}3. {Fore.RESET}Erase data \u2654 \u265a \u2654 .")
        print(
            f"\u265f\u2659 "
            f"Press '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}' to exit and close application "
            f"\u2659\u265f."
        )

        choice = input(f"{Fore.LIGHTYELLOW_EX}Choose an option : {Fore.RESET}")
        if isinstance(choice, str):
            choice = choice.upper()
        return choice
