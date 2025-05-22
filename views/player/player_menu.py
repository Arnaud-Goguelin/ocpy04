from colorama import Fore

from utils import CANCELLED_INPUT, print_title


class PlayerMenuView:

    @staticmethod
    def display():
        print_title("\u265d  Player Menu \u2657 :")

        print(f"{Fore.LIGHTYELLOW_EX}1.{Fore.RESET} Add New Player \u265d.")
        print(f"{Fore.LIGHTYELLOW_EX}2.{Fore.RESET} View Player List \u265c. ")
        print(
            f"\u265f\u2659 "
            f"Press '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}' to return to Main menu "
            f"\u2659\u265f."
        )

        return input(f"{Fore.LIGHTYELLOW_EX}Choose an option : {Fore.RESET_ALL}")