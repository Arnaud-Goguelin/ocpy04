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

    @staticmethod
    def select_tournament_in_list(tournaments: list[Tournament], choice: int | None) -> Tournament | None:

        if isinstance(choice, str) and choice.upper() == CANCELLED_INPUT:
            return None

        if not choice.isdigit():
            print(
                f"\n{Fore.RED}Invalid index. Please enter a {Fore.LIGHTYELLOW_EX}valid tournament's index{Fore.RED} or press '{Fore.LIGHTYELLOW_EX}Enter{Fore.RED}' or '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RED}' to exit the menu.{Fore.RESET}"
                )

        tournament = None
        tournament_index = int(choice) - 1

        if not 0 <= tournament_index < len(tournaments):
            print(
                f"\n{Fore.RED}Invalid index. Please enter a {Fore.LIGHTYELLOW_EX}valid tournament's index{Fore.RED} or press '{Fore.LIGHTYELLOW_EX}Enter{Fore.RED}' or '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RED}' to exit the menu.{Fore.RESET}"
                )
        else:
            tournament = tournaments[tournament_index]

        if not tournament:
            countdown(GenericMessages.TOURNAMENT_MENU_RETURN.value)

        return tournament

    def display_tournament_details(self) -> True:
        try:
            sorted_alphabetically_tournament_list = sorted(
                # use a copy to not alter original data
                self.data.tournaments.copy(),
                key=lambda tournament: tournament.name,
            )
            choice = TournamentListView.handle_tournaments_list(sorted_alphabetically_tournament_list)

            tournament = self.select_tournament_in_list(sorted_alphabetically_tournament_list, choice)

            TournamentDetailsView.display_tournament_details(tournament, True)

        except (TypeError, IndexError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)

        # always return True to stay in this menu
        finally:
            return True

    @staticmethod
    def solve_matches(tournament: Tournament) -> None:
        print("="*10, "nb of match to solve = ", tournament.rounds[-1].match_count, "="*10,)
        last_round = tournament.rounds[-1]
        for match in last_round.matches:
            # TODO: print round name and current match
            print(f"{Fore.LIGHTYELLOW_EX}---{Fore.RESET} {last_round.name} {Fore.LIGHTYELLOW_EX}---{Fore.RESET}")
            choice = MatchDetailsView.display_match_details(match)

            if not choice.isdigit() and choice.upper() != CANCELLED_INPUT:
                print(
                    f"\n{Fore.RED}Invalid index. Please enter a {Fore.LIGHTYELLOW_EX}valid option{Fore.RESET} or press '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' or '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}' to exit the menu.{Fore.RESET}"
                    )

            if choice.upper() == CANCELLED_INPUT:
                countdown(GenericMessages.TOURNAMENT_MENU_RETURN.value)

            match_result = {
                "1": match.player1_wins,
                "2": match.player2_wins,
                "3": match.draw,
                }

            match_result.get(choice, lambda: print_invalid_option([key for key in match_result.keys()]))()
            MatchDetailsView.display_winner(match)

        return last_round.is_round_finished

    def start_or_continue_tournament(self) -> True:
        try:
            # filter tournaments to find those to be start or continue
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

            choice = TournamentListView.handle_tournaments_list(sorted_alphabetically_tournament_list)

            tournament = self.select_tournament_in_list(sorted_alphabetically_tournament_list, choice)

            TournamentDetailsView.display_tournament_details(tournament, False)

            if tournament.rounds_count == 0:
                tournament.start()
            else:
                tournament.continue_tournament()

            are_all_rounds_finished = False
            while not are_all_rounds_finished:
                is_current_round_finished = False
                while not is_current_round_finished:
                    is_current_round_finished = self.solve_matches(tournament)
                tournament.continue_tournament()
                are_all_rounds_finished = all(round.is_round_finished for round in tournament.rounds)

            tournament.end()
            print(f"{Fore.GREEN} Tournament with {len(tournament.players)} players, ends after {tournament.rounds_count} rounds and {sum(round.match_count for round in tournament.rounds)} matches.")
            # return True to stay in this menu
            return True
        except (TypeError, IndexError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)
            self.view.display()

    def exit_tournament_controller(self) -> False:
        # go back to the main menu and main controller
        return False
