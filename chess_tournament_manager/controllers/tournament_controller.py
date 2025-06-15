from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Data

from ..utils import (
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
SolveMatchChoices,
print_tournament_not_saved,
    )
from ..models import Tournament
from ..views import (
    TournamentMenuView,
    CreateTournamentView,
    TournamentListView,
    PlayerListView,
    TournamentDetailsView,
    MatchDetailsView,
)


class TournamentController:
    """
    Controller for managing tournament functionality.

    This class acts as a controller for handling all operations related to tournaments, including
    creating tournaments, displaying tournament details, managing tournament progress, and solving
    matches. It provides methods to interact with the tournament main menu, perform tournament-related
    actions, and manage data related to tournaments.

    Attributes:
        data (Data): An instance of the data model used for storing and retrieving persistent data.
        view (TournamentMenuView): The view associated with displaying the tournament menu interface.
        menu_actions (dict): A dictionary mapping user menu choices to corresponding action methods, where
            the keys are menu options and the values are callable methods to perform those actions.
    """

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
        """
        Controls the flow of the tournament menu and delegates functionality based on user choice.

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
                print_invalid_option(get_menus_keys(self.menu_actions), False, GenericMessages.TOURNAMENT_MENU_RETURN)

    def create_tournament(self) -> True:
        """
        Creates a tournament by selecting players and defining tournament details. The method
        follows a systematic process of allowing player selection from the existing list, applying
        validation to ensure correct inputs, and capturing tournament information.
        Upon successful creation, the new tournament is stored into
        the system's data repository.

        Returns:
            bool: Always returns True to ensure the function caller remains in the corresponding menu.

        Raises:
            ValueError: Raised when invalid input values are encountered during player selection or
                tournament creation process.
            TypeError: Raised when invalid data type operations occur during the flow of tournament creation.
        """
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


            if not selected_players:
                countdown(GenericMessages.TOURNAMENT_MENU_RETURN)
            else:
                # validate players here before display next form to avoid too many inputs
                # and then raise an error concerning the first input
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
        """
        Selects a tournament from a given list of tournaments. It displays a list of tournaments,
        allows the user to select one, and validates the selection.

        Args:
            tournaments: A list of Tournament objects to select from.

        Returns:
            A Tournament object selected by the user if a valid choice is made.
            Returns None if the selection process is cancelled or no valid
            choice is provided.
        """
        tournament = None
        try:
            while not tournament:
                choice = TournamentListView.handle_tournaments_list(tournaments)
                if not choice or (not choice.isdigit() and choice.upper() == CANCELLED_INPUT):
                    break
                tournament_index = int(choice) - 1
                tournament = tournaments[tournament_index]
            return tournament
        except (ValueError, IndexError):
            print_invalid_option(menus_keys=get_menus_keys(tournaments), optional_choices=True)

    def display_tournament_details(self) -> True:
        """
        Displays details of a selected tournament.

        This method is responsible for sorting the list of tournaments by their name,
        allowing the user to select one of them, and displaying detailed information
        about the selected tournament. It guarantees no alteration to the original
        tournaments list by using a copy for sorting.

        Returns:
            bool: Always returns True to indicate that the menu should not exit,
            allowing for further actions.
        """
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
    def solve_matches(tournament: Tournament) -> tuple[bool, bool]:
        """
        Handles the process of solving matches for the last round of a tournament
        by interacting with user input.

        Args:
            tournament: The Tournament object for which the matches in the last round
                need to be solved.
        """
        last_round = tournament.get_last_round
        user_cancelled = False
        for match in last_round.matches:
            if not match.is_match_finished:
                choice = MatchDetailsView.display_match_details(last_round, match)

                check_choice(choice, [*SolveMatchChoices])

                if isinstance(choice, str) and choice.upper() == CANCELLED_INPUT:
                    countdown(GenericMessages.TOURNAMENT_MENU_RETURN)
                    user_cancelled = True
                    break

                match_result = {
                    SolveMatchChoices.PLAYER_1.value: match.player1_wins,
                    SolveMatchChoices.PLAYER_2.value: match.player2_wins,
                    SolveMatchChoices.DRAW.value: match.draw,
                }

                match_action = match_result.get(choice, lambda: print_invalid_option(get_menus_keys(match_result)))
                match_action()
                MatchDetailsView.display_winner(match)

        return last_round.is_round_finished, user_cancelled

    def start_or_continue_tournament(self) -> True:
        """
        Starts or continues a tournament based on its current state and user selection.

        This method identifies tournaments to either start or continue by filtering those
        with missing start or end dates. The user selects the desired tournament to proceed with,
        and the tournament will either start from the beginning or continue if it was
        previously in progress. It iterates through tournament rounds until all rounds are finished.
        Upon completion, the tournament data is saved, ensuring persistence. If no tournament
        is available to start or continue, an exception is raised. It also handles errors encountered
        during this process.

        Returns:
            bool: Always returns True to allow continuing in the current menu context.

        Raises:
            ValueError: Raised when no tournaments are available to start or continue.
            TypeError: Raised during unexpected type handling errors.
            IndexError: Raised when accessing invalid indices.
        """
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
                user_cancelled = False

                while not are_all_rounds_finished and not user_cancelled:
                    is_current_round_finished = False
                    while not is_current_round_finished:
                        is_current_round_finished, user_cancelled = self.solve_matches(tournament)
                        if user_cancelled:
                            print_tournament_not_saved()
                            tournament.reset()
                            break
                    tournament.continue_tournament()
                    are_all_rounds_finished = all(tournament_round.is_round_finished for tournament_round in tournament.rounds)

                if user_cancelled:
                    return True
                else:
                    tournament.end()
                    self.data.save(DataFilesNames.TOURNAMENTS_FILE)
                    print_end_of_tournament(tournament)
            # return True to stay in this menu
            return True
        except (ValueError, TypeError, IndexError) as error:
            print_error(error, GenericMessages.TOURNAMENT_MENU_RETURN)

    def exit_tournament_controller(self) -> False:
        """
        Return to the main menu and main controller flow.

        Returns:
            bool: Always returns False to indicate termination of the current controller
            and transition back to the previous menu or process.
        """
        # go back to the main menu and main controller
        return False
