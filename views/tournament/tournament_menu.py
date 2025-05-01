from utils import CANCELLED_INPUT


class TournamentMenuView:

    @staticmethod
    def display():
        print(
            """
==================================================
\u265e  Tournament Menu \u2658 :
=================================================="""
        )

        print(
            f"1. Create new tournament \u265b."
            f"\n2. View tournament details \u265c."
            f"\n3. Continue tournament \u265e."
            f"\n\u265f\u2659 Press '{CANCELLED_INPUT}' to return to Main menu \u2659\u265f."
        )
