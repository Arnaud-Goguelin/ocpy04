from typing import TYPE_CHECKING

from colorama import Fore

from chess_tournament_manager.utils import CANCELLED_INPUT

if TYPE_CHECKING:
    from chess_tournament_manager.models.match import Match
    from chess_tournament_manager.models.round import Round


class MatchDetailsView:
    """
    Represents a view for displaying details about matches and their outcomes in a tournament context.
    """

    @staticmethod
    def display_match_details(last_round: "Round", match: "Match"):
        """
        Displays the details of a specific match within a round,
        as well as the number of unresolved matches remaining in
        the round. Offers options to resolve the match, mark it as a draw,
        or return to the tournament menu. This method
        is designed for interactive scenarios to navigate match outcomes.

        Args:
            last_round (Round): The current round, containing the details of all matches
                and the overall status of the round.
            match (Match): The specific match to be displayed, containing the participating
                players' information and the match state.

        Returns:
            str: User input that specifies an action to perform, such as choosing a winner,
                marking the match as a draw, or exiting to the tournament menu.
        """

        unsolved_matches = sum(1 for match in last_round.matches if not match.is_match_finished)
        print(
            "=" * 10,
            "nb of match to solve: ",
            unsolved_matches,
            " / ",
            last_round.match_count,
            "=" * 10,
        )

        print()
        print(f"{Fore.LIGHTYELLOW_EX}---{Fore.RESET} {last_round.name} {Fore.LIGHTYELLOW_EX}---{Fore.RESET}")
        print(
            f"{Fore.LIGHTYELLOW_EX}---{Fore.RESET} {match.player1.last_name} vs "
            f"{match.player2.last_name} {Fore.LIGHTYELLOW_EX}---{Fore.RESET}"
        )
        print("Who wins this match?")
        print(f"{Fore.LIGHTYELLOW_EX}1.{Fore.RESET} {match.player1.last_name}")
        print(f"{Fore.LIGHTYELLOW_EX}2.{Fore.RESET} {match.player2.last_name}")
        print(f"{Fore.LIGHTYELLOW_EX}3.{Fore.RESET} Draw")
        print()
        print(
            f"\nSolve match: {Fore.LIGHTYELLOW_EX}copy index{Fore.RESET} / "
            f"Go back to Tournament Menu without saving, press '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}':"
        )

        return input(f"\n{Fore.LIGHTYELLOW_EX}What would you like to do?{Fore.RESET} ")

    @staticmethod
    def display_winner(match: "Match"):
        """
        Displays the winner of a match or indicates if the match was a draw.
        Args:
            match (Match): An instance of the Match class containing details of
                the match, including players and their scores.
        """
        if match.score_player1 > match.score_player2:
            print(f"{Fore.GREEN}{match.player1.last_name} wins!{Fore.RESET}")
        if match.score_player1 < match.score_player2:
            print(f"{Fore.GREEN}{match.player1.last_name} wins!{Fore.RESET}")
        if (match.score_player1 == match.score_player2) and (match.score_player1 > 0 and match.score_player2 > 0):
            print(f"{Fore.YELLOW}{match.player1.last_name} It's a draw{Fore.RESET}")
        return None
