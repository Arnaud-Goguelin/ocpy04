class CreateTournamentView:

    @staticmethod
    def display_choose_players(players: list[str]):
        print(
            """
==================================================================
\u265b  Select players to participate to new tournament   \u2655 :
==================================================================
"""
        )

    @staticmethod
    def display_add_tournament_form():
        print(
            """
==================================================
\u265b  Create a new Tournament   \u2655 :
==================================================
"""
        )

        name = input("Tournament's name : ")
        location = input("Location : ")
        description = input("Description : ")

        return name, location, description
