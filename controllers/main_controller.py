# need to import others controllers with an absolut path to avoid the circular import issue.
from typing import TYPE_CHECKING

from .player.player_controller import PlayerController
from .tournament.tournament_controller import TournamentController

if TYPE_CHECKING:
    from main import Data
from utils import GenericMessages, CANCELLED_INPUT, print_invalid_option, print_error
from views import MainMenuView


class MainController:
    def __init__(self, data: "Data"):
        self.data = data
        self.view = MainMenuView()
        self.menu_actions = {
            "1": self.handle_player_menu,
            "2": self.handle_tournament_menu,
            CANCELLED_INPUT: self.exit_app,
        }

    def handle_main_menu(self):
        while True:
            choice = self.view.display()

            if choice not in self.menu_actions.keys():
                # no error raising here to stay in this menu and avoid redirection to main menu
                print_invalid_option([key for key in self.menu_actions.keys()])

            action = self.menu_actions.get(choice)
            try:
                # action() return True to stay in this menu
                # exit choice exit app in this controller
                return action()
            except Exception as error:
                print_error(error, GenericMessages.MAIN_MENU_RETURN)

    def handle_player_menu(self) -> True:
        try:
            # TODO: why not use class method or static method?
            player_controller = PlayerController(self.data)
            player_controller.handle_player_main_menu()
        except Exception:
            # no error handling here as it is done in handle_main_menu
            # in order to handle errors coming from other controllers too
            pass

    def handle_tournament_menu(self) -> True:
        try:
            tournament_controller = TournamentController(self.data)
            tournament_controller.handle_tournament_main_menu()
        except Exception:
            # no error handling here as it is done in handle_main_menu
            # in order to handle errors coming from other controllers too
            pass

    def exit_app(self) -> None:
        print(GenericMessages.EXIT_MESSAGE.value)
        exit(0)
