from typing import TYPE_CHECKING

from colorama import Fore

from utils import CANCELLED_INPUT

if TYPE_CHECKING:
    from models.match import Match


class MatchDetailsView:

    @staticmethod
    def display_match_details(match: "Match"):
        print()
        print(f"{match.player1.last_name} vs {match.player2.last_name}")
        print()
        print("Who wins this match?")
        print(f"{Fore.LIGHTYELLOW_EX}1.{Fore.RESET} {match.player1.last_name}")
        print(f"{Fore.LIGHTYELLOW_EX}2.{Fore.RESET} {match.player2.last_name}")
        print(f"{Fore.LIGHTYELLOW_EX}3.{Fore.RESET} Draw")
        print()
        print(
            f"\nSelect a player: {Fore.LIGHTYELLOW_EX}copy index{Fore.RESET} / "
            f"Go back to Tournament Menu without saving, press '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}':"
        )
        input(f"\n{Fore.LIGHTYELLOW_EX}What would you like to do?{Fore.RESET} ")