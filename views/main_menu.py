from utils import CANCELLED_INPUT


class MainMenuView:

    @staticmethod
    def display():
        print(
            """
==================================================
\u265a  Welcome to the Chess Tournament Manager \u2654 :
==================================================
"""
        )

        print(
            f"1. Manage Players \u265d."
            f"\n2. Manage Tournaments \u265E."
            f"\n\u265F\u2659 Press '{CANCELLED_INPUT}' to exit and close application \u2659\u265F."
        )
