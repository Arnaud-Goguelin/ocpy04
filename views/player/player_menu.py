from colorama import Fore

from utils import CANCELLED_INPUT, print_title


class PlayerMenuView:
    """
    Represents a view for the Player Menu interface in the application.
    """

    @staticmethod
    def display():
        """
        Displays the Player Menu interface with various menu options and handles user
        input.

        Returns:
            str: The user's choice from the menu (uppercased if it is a string input).
        """
        print_title("\u265d  Player Menu \u2657 :")

        print(f"{Fore.LIGHTYELLOW_EX}1.{Fore.RESET} Add New Player \u265d.")
        print(f"{Fore.LIGHTYELLOW_EX}2.{Fore.RESET} View Player List \u265c. ")
        print(
            f"\u265f\u2659 "
            f"Press '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}' to return to Main menu "
            f"\u2659\u265f."
        )

        choice = input(f"{Fore.LIGHTYELLOW_EX}Choose an option : {Fore.RESET}")
        if isinstance(choice, str):
            choice = choice.upper()
        return choice
