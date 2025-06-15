from typing import TYPE_CHECKING

from colorama import Fore

from chess_tournament_manager.utils import print_title

if TYPE_CHECKING:
    from chess_tournament_manager.models.tournament import Tournament
    from chess_tournament_manager.models.round import Round


class TournamentDetailsView:
    """
    Displays tournament details and rounds.
    """

    @staticmethod
    def display_round_details(tournament_round: "Round"):
        """
        Displays details of a tournament round including the names of players and match outcomes. The method
        renders player names in different colors depending on the match results - green for the winner and
        yellow for a tie.

        Args:
            tournament_round (Round): The tournament round object containing match details.

        """
        print(f"{tournament_round.name}:")
        for i, match in enumerate(tournament_round.matches, 1):
            print(f"Match {i}:")
            if match.score_player1 > match.score_player2:
                print(f" {Fore.GREEN}{match.player1.last_name}{Fore.RESET} vs {match.player2.last_name}")
            if match.score_player1 < match.score_player2:
                print(f" {Fore.GREEN}{match.player2.last_name}{Fore.RESET} vs {match.player1.last_name}")
            if match.score_player1 == match.score_player2:
                print(
                    f" {Fore.YELLOW}{match.player1.last_name}{Fore.RESET} vs "
                    f"{Fore.YELLOW}{match.player2.last_name}{Fore.RESET}"
                )

    @classmethod
    def display_tournament_details(cls, tournament: "Tournament", used_for_details_report: bool = False) -> None:
        """
        Displays detailed information about a tournament
        in a user-interactive manner and optionally allows a pause for user confirmation when used for reports.

        Args:
            tournament (Tournament): The Tournament object containing all the tournament details to display.
            used_for_details_report (bool): Whether the display is part of a detailed report. If True, pauses for user
                confirmation before returning. Defaults to False.

        Returns:
            None
        """
        print_title("\u265c Tournament Details \u2656 :")
        print()
        print(f"Name: {tournament.name}")
        print(f"Location: {tournament.location}")
        print(f"Description: {tournament.description}")
        print(f"Start Date: {tournament.start_date if tournament.start_date else 'To begin'}")
        print(f"End Date: {tournament.end_date if tournament.end_date else 'Not finished'}")
        print(f"Number of Rounds: {tournament.rounds_count if tournament.rounds_count else 0}")
        print()
        print("Players:")

        players = sorted(
            # use a copy to alter original data
            tournament.players,
            key=lambda player: player.last_name,
        )
        player_scores = tournament.get_player_scores()
        for player in players:
            print(
                f"{Fore.LIGHTYELLOW_EX}{players.index(player) + 1}{Fore.RESET}. "
                f"{player.last_name} {player.first_name} - score: {player_scores[player]} "
            )

        print()

        if tournament.start_date:
            print("Rounds:")
            print(
                f"Reminder: winner are in {Fore.GREEN}green{Fore.RESET}, "
                f"looser in white, {Fore.YELLOW}draw{Fore.RESET} in yellow"
            )
            for tournament_round in tournament.rounds:
                cls.display_round_details(tournament_round)

        if used_for_details_report:
            input(f"\nPress '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' to go back to Tournament Menu")
            return None

        return None
