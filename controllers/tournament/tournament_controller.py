from typing import TYPE_CHECKING

from colorama import Fore, Style

if TYPE_CHECKING:
    from main import Data

from utils import countdown, GenericMessages, CANCELLED_INPUT, print_error, print_invalid_option
from models import Tournament
from views import TournamentMenuView, CreateTournamentView, TournamentListView, PlayerListView


class TournamentController:
    def __init__(self, data: "Data"):
        self.data = data
        self.view = TournamentMenuView()
        self.menu_actions = {
            "1": self.create_tournament,
            "2": self.display_tournament_details,
            "3": self.continue_tournament,
            CANCELLED_INPUT: self.exit_tournament_controller,
        }

    def handle_tournament_main_menu(self):
        while True:
            self.view.display()
            choice = input(f"{Fore.LIGHTYELLOW_EX}Choose an option : {Style.RESET_ALL}")
            action = self.menu_actions.get(choice)
            if action:
                # action() return True to stay in this menu or False to got back to main menu
                should_we_stay_in_this_menu = action()
                if not should_we_stay_in_this_menu:
                    return None
            else:
                # no error raising here to stay in this menu and avoid redirection to main menu
                print_invalid_option([key for key in self.menu_actions.keys()])

    def create_tournament(self) -> True:
        try:
            # use a copy of data.players as some players will be removed from the list,
            # we shouldn't alter original data
            players = PlayerListView.handle_players_list(self.data.players.copy(), True)
            # validate players here before display next form to avoid too many inputs
            # and then raise an error concerning the first input
            Tournament.validate_players(players)

            if not players:
                countdown(GenericMessages.TOURNAMENT_MENU_RETURN.value)
            else:
                name, location, description = CreateTournamentView.display_add_tournament_form()

                new_tournament = Tournament(
                    name=name,
                    location=location,
                    description=description,
                    players=players,
                )

                self.data.tournaments.append(new_tournament)

                print(
                    f"{Fore.GREEN}\n\u2655 \u265b \u2655 "
                    f"New tournament {name} created with success ! "
                    f"\u265b \u2655 \u265b .{Fore.RESET}"
                )

        except (ValueError, TypeError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)

        # always return True to stay in this menu
        finally:
            return True

    def display_tournament_details(self) -> True:
        try:
            sorted_alphabetically_tournament_list = sorted(
                # use a copy to not alter original data
                self.data.tournaments.copy(),
                key=lambda tournament: tournament.name,
            )
            TournamentListView.display_tournaments_list(sorted_alphabetically_tournament_list)

        except (TypeError, IndexError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)

        # always return True to stay in this menu
        finally:
            return True

    def continue_tournament(self) -> True:
        try:
            # return True to stay in this menu
            return True
            # TODO: continue or begin tournament + rename option in menu
        except (TypeError, IndexError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)
            self.view.display()

    def exit_tournament_controller(self) -> False:
        # go back to the main menu and main controller
        return False
