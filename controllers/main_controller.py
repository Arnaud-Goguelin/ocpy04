# need to import others controllers with an absolut path to avoid the circular import issue.
from typing import TYPE_CHECKING

from controllers.player.player_controller import PlayerController

if TYPE_CHECKING:
    from main import Data
from utils import EXIT_MESSAGE
from views import MainMenuView


class MainController:
    def __init__(self, data: 'Data'):
        self.data = data
        self.view = MainMenuView()

    def handle_main_menu(self):
        self.view.display()
        choice = input("Choose an option : ")
        if choice == "1":
            player_controller = PlayerController(self.data)
            player_controller.handle_player_main_menu()
        elif choice == "2":
            pass
        elif choice == "3":
            print(EXIT_MESSAGE)
            exit(0)
        else:
            raise ValueError("Invalid option, please choose between 1, 2 or 3.")
