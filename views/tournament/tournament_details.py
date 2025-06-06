from typing import TYPE_CHECKING

from colorama import Fore

from utils import print_title

if TYPE_CHECKING:
    from models.tournament import Tournament
    from models.round import Round


class TournamentDetailsView:

    @staticmethod
    def display_round_details(tournament_round: "Round"):
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

        players = tournament.rank_players()
        player_scores = tournament.get_player_scores()
        players.reverse()
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
