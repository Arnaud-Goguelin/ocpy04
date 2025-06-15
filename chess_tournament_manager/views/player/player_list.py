from typing import TYPE_CHECKING

from colorama import Fore

from chess_tournament_manager.utils import (
    CANCELLED_INPUT,
    print_title,
    )

if TYPE_CHECKING:
    from chess_tournament_manager.models.player import Player


class PlayerListView:
    """
    Represents the view for displaying and interacting with a list of players in different
    contexts such as viewing player details or selecting players for creating tournaments.
    """

    @staticmethod
    def display_players_list(players: list["Player"]):
        """
        Displays a formatted list of players and their relevant information.

        Args:
            players (list[Player]): A list of Player objects to be displayed.

        Raises:
            ValueError: If the provided list of players is empty.
        """

        if not players:
            raise ValueError("No players to display.")

        for player in players:
            print(
                f"{Fore.LIGHTYELLOW_EX}{players.index(player) + 1}{Fore.RESET}. "
                f"{player.last_name} {player.first_name}, "
                f"{player.birthdate} - {player.chess_id}"
            )

    @classmethod
    def handle_players_list(
        cls, players: list["Player"], used_for_selecting_players: bool = False, last_selected_player: "Player" = None
    ) -> str | None:
        """
        Handles the display and selection of players for a list shown in a specific context,
        either for viewing player details or for selecting them in preparation for a new
        tournament.

        Args:
            players: List of "Player" objects to be displayed or selected from.
            used_for_selecting_players: Flag indicating whether the list is being used to
                select players for creating a new tournament or just for displaying player
                details.
            last_selected_player: The last "Player" object selected, used to inform the
                user about previously selected players when adding more players to the
                tournament.

        Returns:
            str | None:
                Returns the user input as a string when operating in selection mode for
                creating a new tournament. Returns None when used for simply displaying
                player details, or when there are no more players to select.

        Raises:
            ValueError: If there are neither players to select nor a last selected
                player, indicating an error scenario when attempting to display or
                select players.
        """

        print_title("\u265d  Players List \u2657 :")

        # --- List used to display player details ---
        if not used_for_selecting_players:
            cls.display_players_list(players)
            input(f"\nPress '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' to go back to Player Menu")
            return None

        # --- List used to select players for a new tournament ---

        if not players and not last_selected_player:
            # if there is no last_selected_player and not players, this is an error
            raise ValueError("No players to display.")

        if not players and last_selected_player:
            # in this case, do not raise error
            # if there is no player but there is a last_selected_player,
            # that means user has already selected all players for a new tournament
            print("\nNo more player to add, continue new tournament creation.")
            return None

        print(
            f"{Fore.LIGHTYELLOW_EX}---{Fore.RESET} "
            f"To create a new tournament, you need to select players. "
            f"{Fore.LIGHTYELLOW_EX}---{Fore.RESET}"
        )
        print()

        if last_selected_player:
            print(
                f"{Fore.GREEN}--- Added: "
                f"{last_selected_player.last_name} {last_selected_player.first_name} "
                f"--- {Fore.RESET}"
            )
            print("\nRemaining players:")

        cls.display_players_list(players)

        return input(
            f"\n{Fore.LIGHTYELLOW_EX}What would you like to do?{Fore.RESET}"
            f"\nSelect a player: {Fore.LIGHTYELLOW_EX}copy index{Fore.RESET} / "
            f"Save and validate choices, press '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' / "
            f"Go back to Tournament Menu without saving, press '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RESET}'\n:"
        )
