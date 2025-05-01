from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Data

from utils import countdown, GenericMessages, CANCELLED_INPUT
from models import Tournament
from views import TournamentMenuView, CreateTournamentView, TournamentListView, PlayerListView


class TournamentController:
    def __init__(self, data: "Data"):
        self.data = data
        self.view = TournamentMenuView()

    def handle_tournament_main_menu(self):
        while True:
            self.view.display()
            choice = input("Choose an option : ")

            if choice == "1":
                try:
                    # use a copy of data.players as some players will be removed from the list,
                    # we shouldn't alter original data
                    players = PlayerListView.handle_players_list(self.data.players.copy(), True)

                    if not players:
                        countdown(GenericMessages.TOURNAMENT_MENU_RETURN.value)
                    else:
                        name, location, description = CreateTournamentView.display_add_tournament_form()
                        print(players)
                        new_tournament = Tournament(
                            name=name,
                            location=location,
                            description=description,
                            players=players,
                        )

                        self.data.tournaments.append(new_tournament)

                        print(
                            f"\n\u2655 \u265b \u2655 "
                            f"New tournament {name} created with success ! "
                            f"\u265b \u2655 \u265b ."
                        )

                except (ValueError, TypeError) as error:
                    print("\nAn error occurred : ")
                    print(error)
                    countdown(GenericMessages.TOURNAMENT_MENU_RETURN.value)
                    self.view.display()

            elif choice == "2":
                try:
                    sorted_alphabetically_tournament_list = sorted(
                        # use a copy to not alter original data
                        self.data.tournaments.copy(),
                        key=lambda tournament: tournament.name,
                    )
                    TournamentListView.display_tournaments_list(sorted_alphabetically_tournament_list)

                except (TypeError, IndexError) as error:
                    print("\nAn error occurred : ")
                    print(error)
                    countdown(GenericMessages.TOURNAMENT_MENU_RETURN.value)
                    self.view.display()

            elif choice == "3":
                try:
                    pass
                    # TODO: continue or begin tournament + rename option in menu
                except (TypeError, IndexError) as error:
                    print("\nAn error occurred : ")
                    print(error)
                    countdown(GenericMessages.TOURNAMENT_MENU_RETURN.value)
                    self.view.display()

            elif choice == CANCELLED_INPUT:
                # go back to the main menu and main controller
                return None

            else:
                print("Invalid option, please choose between 1, 2, 3 or 4.")
