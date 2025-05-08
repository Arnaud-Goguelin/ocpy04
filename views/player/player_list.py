from typing import TYPE_CHECKING

from colorama import Fore

from utils import CANCELLED_INPUT, print_title

if TYPE_CHECKING:
    from models.player import Player


class PlayerListView:

    @staticmethod
    def display_players_list(players: list["Player"]):
        for player in players:
            print(
                f"{Fore.LIGHTYELLOW_EX}{players.index(player) + 1}{Fore.RESET}. "
                f"{player.last_name} {player.first_name}, "
                f"{player.birthdate} - {player.chess_id}"
            )

    @classmethod
    def handle_players_list(cls, players: list["Player"], is_used_for_selecting_players: bool = False):
        """
        Displays a list of players and allows for optional selection of players based on user input.

        If the `is_used_for_selecting_players` flag is set to False, the function displays the list of players
        without user interaction for selection. The user can view the list and press 'Enter' to return
        to the Player Menu.
        If the list of `players` is empty, a ValueError will be raised.

        If the `is_used_for_selecting_players` flag is set to True, it enables the selection mode where the user
        can select players from the displayed list by index. Duplicate selections are not allowed (thanks to set()).
        The user can choose to exit the selection mode by entering 'Esc',
        or complete the selection process by pressing 'Enter' without choosing more players.

        :param players: The list of "Player" objects to be displayed and optionally selected.
        :param is_used_for_selecting_players: Determines the mode of operation.
        :return: A set of selected "Player" objects if `is_used_for_selecting_players` is True; otherwise None.
        """
        print_title("\u265d  Players List \u2657 :")

        if not players:
            raise ValueError("No players to display.")

        # --- List used to display player details ---
        if not is_used_for_selecting_players:
            cls.display_players_list(players)
            input(f"\nPress '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' to go back to Player Menu")
            return None

        # --- List used to select players for a new tournament ---
        print("To create a new tournament, you need to select players.")

        # countdown(GenericMessages.PLAYER_LIST.value)

        # use a set() to avoid duplicate
        selected_players = set()
        cls.display_players_list(players)
        while True:

            if not players:
                print("\nNo more player to add, continue new tournament creation.")
                return selected_players

            choice = input(
                f"\n{Fore.LIGHTYELLOW_EX}What would you like to do?{Fore.RESET}"
                f"\nSelect a player: {Fore.LIGHTYELLOW_EX}copy index{Fore.RESET} / "
                f"Save and validate choices, press '{Fore.LIGHTYELLOW_EX}Enter{Fore.RESET}' / "
                f"Go back to Tournament Menu without saving, press '{Fore.LIGHTYELLOW_EX}q{Fore.RESET}'\n:"
            )

            if choice.lower() == CANCELLED_INPUT:
                print("\nA tournament need players, cancel new Tournament creation.")
                return None

            elif choice == "":

                if not selected_players:
                    print("\nNo player selected, cancel new Tournament creation.")
                    return None

                return selected_players

            elif not choice.isdigit():
                print(
                    "\nInvalid index. Please enter a valid player's index or press 'Enter' or 'Esc' to exit the menu."
                )

            else:
                player_index = int(choice) - 1

                if not 0 <= player_index < len(players):
                    print(
                        "\nInvalid index. Please enter a valid player's index "
                        "or press 'Enter' or 'Esc' to exit the menu."
                    )

                else:
                    selected_player = players[player_index]
                    selected_players.add(selected_player)
                    print(f"Added: {selected_player.last_name} {selected_player.first_name}")
                    print("\nRemaining players:")
                    players.remove(selected_player)
                    cls.display_players_list(players)
