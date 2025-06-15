from colorama import Fore

from chess_tournament_manager.models import Player, Tournament


def print_creation_success(object: Player | Tournament) -> None:
    """
    Prints a success message upon the creation of a Class object.
    Args:
        object (Player | Tournament): The instance of the object that has been created. The object should
            be either a Player or a Tournament.

    """

    if isinstance(object, Tournament):
        start_symbols = "\u2655 \u265b \u2655"
        end_symbols = "\u265b \u2655 \u265b"
        object_type = type(object).__name__
        object_name = object.name

    if isinstance(object, Player):
        start_symbols = "\u2657 \u265d \u2657"
        end_symbols = "\u265d \u2657 \u265d"
        object_type = type(object).__name__
        object_name = f"{object.first_name} {object.last_name}"

    print(
        f"{Fore.GREEN}\n{start_symbols} "
        f"New {object_type} {object_name} created with success ! "
        f"{end_symbols} .{Fore.RESET}"
    )
    return None


def print_end_of_tournament(tournament: Tournament) -> None:
    """
    Prints a summary at the end of a tournament.
    """
    print(
        f"{Fore.GREEN} Tournament with {len(tournament.players)} players, "
        f"ends after {tournament.rounds_count} rounds "
        f"and {sum(round.match_count for round in tournament.rounds)} matches."
    )
