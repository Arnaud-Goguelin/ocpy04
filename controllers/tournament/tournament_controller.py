from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Data

from utils import (
    DataFilesNames,
    countdown,
    GenericMessages,
    CANCELLED_INPUT,
    print_error,
    print_invalid_option,
    print_creation_success,
    get_menus_keys,
    print_end_of_tournament,
    check_choice,
)
from models import Tournament
from views import (
    TournamentMenuView,
    CreateTournamentView,
    TournamentListView,
    PlayerListView,
    TournamentDetailsView,
    MatchDetailsView,
)


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
                print_invalid_option(get_menus_keys(self.menu_actions), False, GenericMessages.TOURNAMENT_MENU_RETURN)

    def create_tournament(self) -> True:
        try:
            # use a copy of data.players as some players will be removed from the list,
            # we shouldn't alter original data
            players = self.data.players.copy()
            # use a set() to avoid duplicate
            selected_players = set()
            selected_player = None

            while players:
                choice = PlayerListView.handle_players_list(
                    players=players,
                    used_for_selecting_players=True,
                    last_selected_player=selected_player,
                )

                if choice.upper() == CANCELLED_INPUT:
                    countdown(GenericMessages.TOURNAMENT_MENU_RETURN)
                    break

                if choice == "":
                    break

                check_choice(choice, players)

                try:
                    player_index = int(choice) - 1
                    selected_player = players[player_index]
                    if selected_player:
                        selected_players.add(selected_player)
                        players.remove(selected_player)
                except (ValueError, IndexError):
                    continue

            # display a message once there is no more players to select
            if not players:
                PlayerListView.handle_players_list(
                    players=players, used_for_selecting_players=True, last_selected_player=selected_player
                )

            # validate players here before display next form to avoid too many inputs
            # and then raise an error concerning the first input
            if not selected_players:
                countdown(GenericMessages.TOURNAMENT_MENU_RETURN)
            else:
                Tournament.validate_players(selected_players)
                name, location, description = CreateTournamentView.display_add_tournament_form()

                new_tournament = Tournament(
                    name=name,
                    location=location,
                    description=description,
                    players=selected_players,
                )

                self.data.tournaments.append(new_tournament)
                self.data.save(DataFilesNames.TOURNAMENTS_FILE)

                print_creation_success(new_tournament)

        except (ValueError, TypeError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)

        # always return True to stay in this menu
        finally:
            return True

    def select_tournament(self, tournaments: list[Tournament]) -> Tournament | None:
        tournament = None
        try:
            while not tournament:
                choice = TournamentListView.handle_tournaments_list(tournaments)
                check_choice(choice, get_menus_keys(tournaments))
                if not choice or (not choice.isdigit() and choice.upper() == CANCELLED_INPUT):
                    break
                tournament_index = int(choice) - 1
                tournament = tournaments[tournament_index]
            return tournament
        except (ValueError, IndexError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)

    def display_tournament_details(self) -> True:
        # sort tournaments by name
        tournaments = sorted(
            # use a copy to not alter original data
            self.data.tournaments.copy(),
            key=lambda tournament: tournament.name,
        )

        tournament = self.select_tournament(tournaments)

        if tournament:
            TournamentDetailsView.display_tournament_details(tournament, True)

        # always return True to stay in this menu
        return True

    @staticmethod
    def solve_matches(tournament: Tournament) -> None:
        last_round = tournament.get_last_round
        for match in last_round.matches:
            choice = MatchDetailsView.display_match_details(last_round, match)

            # exceptionally, as the menu is in a view, we have to copy it here
            check_choice(choice, ["1", "2", "3"])

            if isinstance(choice, str) and choice.upper() == CANCELLED_INPUT:
                countdown(GenericMessages.TOURNAMENT_MENU_RETURN)
                break

            match_result = {
                "1": match.player1_wins,
                "2": match.player2_wins,
                "3": match.draw,
            }

            match_action = match_result.get(choice, lambda: print_invalid_option(get_menus_keys(match_result)))
            match_action()
            MatchDetailsView.display_winner(match)

        return last_round.is_round_finished

    def start_or_continue_tournament(self) -> True:
        try:
            # filter tournaments to find those to be start or continue
            concerned_tournaments = [
                tournament
                for tournament in self.data.tournaments
                if tournament.start_date is None or tournament.end_date is None
            ]
            tournaments = sorted(
                # use a copy to not alter original data
                concerned_tournaments,
                key=lambda tournament: tournament.name,
            )

            if not tournaments:
                raise ValueError("No tournament to start or continue.")

            tournament = self.select_tournament(tournaments)

            if tournament:

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
                self.data.save(DataFilesNames.TOURNAMENTS_FILE)
                print_end_of_tournament(tournament)
            # return True to stay in this menu
            return True
        except (ValueError, TypeError, IndexError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)

    def exit_tournament_controller(self) -> False:
        # go back to the main menu and main controller
        return False
