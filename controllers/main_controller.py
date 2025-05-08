# need to import others controllers with an absolut path to avoid the circular import issue.
from typing import TYPE_CHECKING

from colorama import Fore, Style

from .player.player_controller import PlayerController
from .tournament.tournament_controller import TournamentController

if TYPE_CHECKING:
    from main import Data
from utils import GenericMessages, CANCELLED_INPUT
from views import MainMenuView


class MainController:
    def __init__(self, data: "Data"):
        self.data = data
        self.view = MainMenuView()

    def handle_main_menu(self):
        self.view.display()
        choice = input(f"{Fore.LIGHTYELLOW_EX}Choose an option : {Style.RESET_ALL}")
        if choice == "1":
            player_controller = PlayerController(self.data)
            player_controller.handle_player_main_menu()
        elif choice == "2":
            tournament_controller = TournamentController(self.data)
            tournament_controller.handle_tournament_main_menu()
        elif choice == CANCELLED_INPUT:
            print(GenericMessages.EXIT_MESSAGE.value)
            exit(0)
        else:
            # no error raising here to avoid countdown and be redirected to main menu
            print(f"{Fore.RED}Invalid option, please choose between 1, 2 or 'q'.{Fore.RESET}")
