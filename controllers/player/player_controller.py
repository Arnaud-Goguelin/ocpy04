from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Data

from utils import countdown
from models.player import Player
from views import PlayerMenuView, CreatePlayerView, PlayerListView


class PlayerController:
    def __init__(self, data: "Data"):
        self.data = data
        self.view = PlayerMenuView()

    def handle_player_main_menu(self):
        while True:
            self.view.display()
            choice = input("Choose an option : ")

            if choice == "1":
                try:
                    first_name, last_name, birthdate, chess_id = CreatePlayerView.display_add_player_form()
                    new_player = Player(
                        first_name=first_name,
                        last_name=last_name,
                        birthdate=birthdate,
                        chess_id=chess_id,
                    )

                    self.data.players.append(new_player)

                    print(
                        f"\n\u2657 \u265d \u2657 "
                        f"New player {first_name} {last_name.upper()} created with success ! "
                        f"\u265d \u2657 \u265d ."
                    )

                except ValueError as error:
                    print("\nAn error occurred : ")
                    print(error)
                    countdown(menu_name="player")
                    self.view.display()

            elif choice == "2":
                try:
                    sort_alphabetically_player_list = sorted(
                        self.data.players.copy(),
                        key=lambda player: player.last_name,
                    )
                    PlayerListView.display_player_list(sort_alphabetically_player_list)

                except (TypeError, IndexError) as error:
                    print("\nAn error occurred : ")
                    print(error)
                    countdown(menu_name="player")
                    self.view.display()

            elif choice == "3":
                # go back to main menu and main controller
                return None

            else:
                print("Invalid option, please choose between 1,2 or 3.")
