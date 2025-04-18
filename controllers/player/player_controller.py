from models.player import Player
from views import PlayerMenuView, CreatePlayerView


class PlayerController:
    def __init__(self):
        self.view = PlayerMenuView()

    def handle_player_main_menu(self):
        while True:
            self.view.display()
            choice = input("Choose an option : ")
            if choice == "1":
                first_name, last_name, birthday, chess_id = CreatePlayerView.display_add_player_form()
                Player(
                    first_name=first_name,
                    last_name=last_name,
                    birthday=birthday,
                    chess_id=chess_id,
                )
                print(
                    f"\n\u2657 \u265D \u2657 "
                    f"New player {first_name} {last_name} created with success ! "
                    f"\u265D \u2657 \u265D .")

            elif choice == "2":
                pass
            elif choice == "3":
                # go back to main menu and main controller
                return None
            else:
                print("Invalid option, please choose between 1,2 or 3.")
