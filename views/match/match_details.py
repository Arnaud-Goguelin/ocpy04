from typing import TYPE_CHECKING

from colorama import Fore

from utils import CANCELLED_INPUT

if TYPE_CHECKING:
    from models.match import Match
    from models.round import Round


class MatchDetailsView:

    @staticmethod
    def display_match_details(last_round: "Round", match: "Match"):
        print()
        print(f"{Fore.LIGHTYELLOW_EX}---{Fore.RESET} {last_round.name} {Fore.LIGHTYELLOW_EX}---{Fore.RESET}")
        print(
            f"{Fore.LIGHTYELLOW_EX}---{Fore.RESET} {match.player1.last_name} vs {match.player2.last_name} {Fore.LIGHTYELLOW_EX}---{Fore.RESET}"
        )
        print("Who wins this match?")
        print(f"{Fore.LIGHTYELLOW_EX}1.{Fore.RESET} {match.player1.last_name}")
        print(f"{Fore.LIGHTYELLOW_EX}2.{Fore.RESET} {match.player2.last_name}")
        print(f"{Fore.LIGHTYELLOW_EX}3.{Fore.RESET} Draw")
        print()
        print(
            f"\nSelect a player: {Fore.LIGHTYELLOW_EX}copy index{Fore.RESET} / "
            f"Go back to Tournament Menu without saving, press '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}':"
        )

        return input(f"\n{Fore.LIGHTYELLOW_EX}What would you like to do?{Fore.RESET} ")

    @staticmethod
    def display_winner(match: "Match"):
        if match.score_player1 > match.score_player2:
            print(f"{Fore.GREEN}{match.player1.last_name} wins!{Fore.RESET}")
        if match.score_player1 < match.score_player2:
            print(f"{Fore.GREEN}{match.player1.last_name} wins!{Fore.RESET}")
        if (match.score_player1 == match.score_player2) and (match.score_player1 > 0 and match.score_player2 > 0):
            print(f"{Fore.YELLOW}{match.player1.last_name} It's a draw{Fore.RESET}")
        return None
