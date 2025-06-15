from colorama import Fore

from chess_tournament_manager.utils import CANCELLED_INPUT, print_title


class TournamentMenuView:
    """
    Represents the view for the Tournament Menu in the application.
    """

    @staticmethod
    def display():
        """
        Displays the Tournament Menu and prompts the user to select an option.

        Returns:
            str: User's input choice from the menu options. Input is converted to uppercase if it is
            a string.
        """
        print_title("\u265e  Tournament Menu \u2658 :")

        print(f"{Fore.LIGHTYELLOW_EX}1{Fore.RESET}. Create new tournament \u265b.")
        print(f"{Fore.LIGHTYELLOW_EX}2{Fore.RESET}. View tournament details \u265c.")
        print(f"{Fore.LIGHTYELLOW_EX}3{Fore.RESET}. Start or continue tournament \u265e.")
        print(
            f"\u265f\u2659 Press "
            f"'{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}' to return to Main menu "
            f"\u2659\u265f."
        )

        choice = input(f"{Fore.LIGHTYELLOW_EX}Choose an option : {Fore.RESET}")
        if isinstance(choice, str):
            choice = choice.upper()
        return choice
