from typing import TYPE_CHECKING

from colorama import Fore, Style

if TYPE_CHECKING:
    from main import Data

from utils import GenericMessages, CANCELLED_INPUT, print_error
from models import Player
from views import PlayerMenuView, CreatePlayerView, PlayerListView


class PlayerController:
    def __init__(self, data: "Data"):
        self.data = data
        self.view = PlayerMenuView()

    def handle_player_main_menu(self):
        while True:
            self.view.display()
            choice = input(f"{Fore.LIGHTYELLOW_EX}Choose an option : {Style.RESET_ALL}")

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
                        f"{Fore.GREEN}\n\u2657 \u265d \u2657 "
                        f"New player {first_name} {last_name.upper()} created with success ! "
                        f"\u265d \u2657 \u265d .{Fore.RESET}"
                    )

                except ValueError as error:
                    print_error(error, GenericMessages.PLAYER_MENU_RETURN)
                    self.view.display()

            elif choice == "2":
                try:
                    sorted_alphabetically_player_list = sorted(
                        # use a copy to alter original data
                        self.data.players.copy(),
                        key=lambda player: player.last_name,
                    )
                    PlayerListView.handle_players_list(sorted_alphabetically_player_list, False)

                except (ValueError, TypeError, IndexError) as error:
                    print_error(error, GenericMessages.PLAYER_MENU_RETURN)
                    self.view.display()

            elif choice == CANCELLED_INPUT:
                # go back to main menu and main controller
                return None

            else:
                # no error raising here or user would be redirected to main menu, it is better to stay here
                print(f"{Fore.RED}Invalid option, please choose between 1, 2 or 'q'.{Fore.RESET}")
