from colorama import Fore

from models import Player, Tournament


# "Player" | "Tournament" with | character is not usable between 2 strings
# it is not compatible with type checking on this case
def print_creation_success(object: Player | Tournament) -> None:

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
