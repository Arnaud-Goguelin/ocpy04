from typing import TYPE_CHECKING

from colorama import Fore

from utils import (
    CANCELLED_INPUT,
    print_title,
    )

if TYPE_CHECKING:
    from models.player import Player


class PlayerListView:

    @staticmethod
    def display_players_list(players: list["Player"]):

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
