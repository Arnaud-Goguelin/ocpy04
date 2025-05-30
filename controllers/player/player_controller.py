from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Data

from utils import (
    GenericMessages,
    CANCELLED_INPUT,
    print_error,
    print_invalid_option,
    print_creation_success,
    DataFilesNames,
)
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
                chess_ids_from_data=[player.chess_id for player in self.data.players],
            )

            self.data.players.append(new_player)
            self.data.save(DataFilesNames.PLAYERS_FILE)
            print_creation_success(new_player)

        except ValueError as error:
            print_error(error, GenericMessages.PLAYER_MENU_RETURN)

        # TODO: finallu bloc here avoid to raise error, in Data.save
        # always return True to stay in this menu
        # finally:
        #     return True

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
