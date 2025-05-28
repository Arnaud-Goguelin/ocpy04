from colorama import Fore

from .constant import CANCELLED_INPUT, GenericMessages
from .countdown import countdown


def print_error(
    error: Exception,
    generic_messages: GenericMessages,
):
    print(f"\n{Fore.RED}An error occurred : {Fore.RESET}")
    print(f"{Fore.RED}{error}{Fore.RESET}")
    countdown(generic_messages.value)


def print_invalid_option(menus_keys: list[str], optional_choices: bool = False):
    print(
        f"{Fore.RED}Invalid option, please choose between :"
        f"{Fore.LIGHTYELLOW_EX}{", ".join(menus_keys)}{Fore.RED}"
        f"{f", or press '{Fore.LIGHTYELLOW_EX}Enter{Fore.RED}' or '{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RED}' to exit" 
        if optional_choices else ""}.{Fore.RESET}"
    )
