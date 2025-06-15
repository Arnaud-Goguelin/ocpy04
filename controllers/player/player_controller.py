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
    """
    Handles the control flow of the player's menu in the application.

    Provides methods to navigate through the player menu options, handle user input,
    and perform actions like creating a new player or displaying the list of players.
    The class ensures seamless interaction between the view, data, and underlying
    application logic for player-related functionalities.

    Attributes:
        data (Data): The data object where player information is stored and managed.
        view (PlayerMenuView): The view object to render and interact with the player menu.
        menu_actions (dict): Dictionary mapping menu options to their respective action methods.
    """

    def __init__(self, data: "Data"):
        self.data = data
        self.view = PlayerMenuView()
        self.menu_actions = {
            "1": self.create_player,
            "2": self.display_players_list,
            CANCELLED_INPUT: self.exit_player_controller,
        }

    def handle_player_main_menu(self):
        """
        Controls the flow of the player menu and delegates functionality based on user choice.

        Returns:
            None: Exits and returns to the main menu when the user chooses to do so or
            a specific condition from an action is met.
        """
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
                print_invalid_option(
                    [key for key in self.menu_actions.keys()], False, GenericMessages.PLAYER_MENU_RETURN
                )

    def create_player(self) -> True:
        """
        Creates a new player by collecting input from the user, validating it, and saving the
        player data to a persistent storage. Handles value errors during input parsing and
        ensures the program remains in the same menu after execution.

        Returns:
            True: Indicates successful handling of the process (irrespective of whether
            the player was created or an error occurred).
        """
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
        """
        Displays a list of players sorted alphabetically by their last names.

        Raises:
            ValueError: If there is an invalid operation related to values in the data.
            TypeError: If there is a type mismatch during operations.
            IndexError: If an indexing operation is attempted on a non-existent element.

        Returns:
            bool: Always returns True to signify remaining in the current menu.
        """
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
        """
        Return to the main menu and main controller flow.

        Returns:
            bool: Always returns False to indicate termination of the current controller
            and transition back to the previous menu or process.
        """
        # go back to the main menu and main controller
        return False
