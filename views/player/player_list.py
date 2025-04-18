from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.player import Player


class PlayerListView:
    @staticmethod
    def display_player_list(players_list: list['Player']):
        print("""
==================================================
\u265D Player List \u2657 :
==================================================""")
        for player in players_list:
            print(
                f"{players_list.index(player) + 1}. {player.last_name} {player.first_name}, "
                f"{player.birthdate} - {player.chess_id}"
            )

        input("\nPress 'Enter' to go back to Player Menu")
