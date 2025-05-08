from colorama import Fore

from .constant import GenericMessages
from .countdown import countdown


def print_error(
    error: Exception,
    generic_messages: GenericMessages,
):
    print(f"\n{Fore.RED}An error occurred : {Fore.RESET}")
    print(f"{Fore.RED}{error}{Fore.RESET}")
    countdown(generic_messages.value)


def print_invalid_option(menus_actions_keys: list[str]):
    print(f"{Fore.RED}Invalid option, please choose between {", ".join(menus_actions_keys)}.{Fore.RESET}")
