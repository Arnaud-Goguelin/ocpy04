from typing import TYPE_CHECKING

from colorama import (
    Fore,
    )

if TYPE_CHECKING:
    from main import Data

from utils import countdown, GenericMessages, CANCELLED_INPUT, \
    print_error, print_invalid_option
from models import Tournament
from views import TournamentMenuView, CreateTournamentView, TournamentListView, PlayerListView, TournamentDetailsView, MatchDetailsView


class TournamentController:
    def __init__(self, data: "Data"):
        self.data = data
        self.view = TournamentMenuView()
        self.menu_actions = {
            "1": self.create_tournament,
            "2": self.display_tournament_details,
            "3": self.start_or_continue_tournament,
            CANCELLED_INPUT: self.exit_tournament_controller,
        }

    def handle_tournament_main_menu(self):
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

    def create_tournament(self) -> True:
        try:
            # use a copy of data.players as some players will be removed from the list,
            # we shouldn't alter original data
            players = PlayerListView.handle_players_list(self.data.players.copy(), True)
            # validate players here before display next form to avoid too many inputs
            # and then raise an error concerning the first input
            if not players:
                countdown(GenericMessages.TOURNAMENT_MENU_RETURN.value)
            else:
                Tournament.validate_players(players)
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
            tournament = TournamentListView.handle_tournaments_list(sorted_alphabetically_tournament_list)
            if not tournament:
                countdown(GenericMessages.TOURNAMENT_MENU_RETURN.value)
                return True
            TournamentDetailsView.display_tournament_details(tournament)

        except (TypeError, IndexError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)

        # always return True to stay in this menu
        finally:
            return True

    @staticmethod
    def solve_matches(tournament: Tournament) -> None:
        for match in tournament.rounds[-1].matches:
            match_choice = MatchDetailsView.display_match_details(match)

            if match_choice.upper() == CANCELLED_INPUT:
                return None

            elif not match_choice.isdigit():
                print(
                    f"\n{Fore.RED}Invalid index. Please enter a valid player's index or press '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' or '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}' to exit the menu.{Fore.RESET}"
                    )
            else:
                index = int(match_choice) - 1
                winner = match.participating_players[index] if index < len(match.participating_players) else None
                match.set_match_score(winner)
        return None

    def start_or_continue_tournament(self) -> True:
        try:
            concerned_tournament = [
                tournament
                for tournament in self.data.tournaments
                if tournament.start_date is None or tournament.end_date is None
            ]
            sorted_alphabetically_tournament_list = sorted(
                # use a copy to not alter original data
                concerned_tournament,
                key=lambda tournament: tournament.name,
            )
            tournament = TournamentListView.handle_tournaments_list(sorted_alphabetically_tournament_list)
            TournamentDetailsView.display_tournament_details(tournament)

            if tournament.rounds_count == 0:
                tournament.start()
            else:
                tournament.continue_tournament()

            are_all_matches_rounds_finished = False
            while not are_all_matches_rounds_finished:
                self.solve_matches(tournament)
                are_all_matches_rounds_finished = all(round.is_finished for round in tournament.rounds)

            # return True to stay in this menu
            return True
        except (TypeError, IndexError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)
            self.view.display()

    def exit_tournament_controller(self) -> False:
        # go back to the main menu and main controller
        return False
