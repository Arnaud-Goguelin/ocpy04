from typing import TYPE_CHECKING

from colorama import Fore

if TYPE_CHECKING:
    from main import Data

from utils import GenericMessages, CANCELLED_INPUT, print_error, print_invalid_option
from models import Player
from views import PlayerMenuView, CreatePlayerView, PlayerListView


class PlayerController:
    def __init__(self, data: "Data"):
        self.data = data
        self.view = PlayerMenuView()
        self.menu_actions = {
            "1": self.create_player,
            "2": self.display_players_list,
            CANCELLED_INPUT: self.exit_player_controller,
        }

    def handle_player_main_menu(self):
        while True:
            choice = self.view.display()
            action = self.menu_actions.get(choice)
            if action:
                # action() return True to stay in this menu or False to got back to main menu
                should_we_stay_in_this_menu = action()
                if not should_we_stay_in_this_menu:
                    return None
            else:
                # no error raising here to stay in this menu and avoid redirection to main menu
                print_invalid_option([key for key in self.menu_actions.keys()])

    def create_player(self) -> True:
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

        # always return True to stay in this menu
        finally:
            return True

    def display_players_list(self) -> True:
        try:
            sorted_alphabetically_player_list = sorted(
                # use a copy to alter original data
                self.data.players.copy(),
                key=lambda player: player.last_name,
            )
            PlayerListView.handle_players_list(sorted_alphabetically_player_list, False)

        except (ValueError, TypeError, IndexError) as error:
            print_error(error, GenericMessages.PLAYER_MENU_RETURN)

        # always return True to stay in this menu
        finally:
            return True

    def exit_player_controller(self) -> False:
        # go back to the main menu and main controller
        return False
