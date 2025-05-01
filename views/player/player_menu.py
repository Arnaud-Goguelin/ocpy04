from utils import CANCELLED_INPUT


class PlayerMenuView:

    @staticmethod
    def display():
        print(
            """
==================================================
\u265d  Player Menu \u2657 :
=================================================="""
        )

        print(
            f"1. Add New Player \u265d."
            f"\n2. View Player List \u265c. "
            f"\n\u265f\u2659 Press '{CANCELLED_INPUT}' to return to Main menu \u2659\u265f."
        )
