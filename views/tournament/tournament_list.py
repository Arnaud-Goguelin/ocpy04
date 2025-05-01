from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.tournament import Tournament


class TournamentListView:
    @staticmethod
    def display_tournaments_list(tournaments: list["Tournament"]):
        print(
            """
==================================================
\u265b Tournaments List \u2655 :
==================================================
"""
        )
        for tournament in tournaments:
            print(
                f"{tournaments.index(tournament) + 1}. {tournament.name} in {tournament.location}, "
                f"{tournament.start_date if tournament.start_date else "To begin"} - "
                f"{tournament.end_date if tournament.end_date else "Not finished"}."
            )

        input("\nPress 'Enter' to go back to Player Menu")
        return None
