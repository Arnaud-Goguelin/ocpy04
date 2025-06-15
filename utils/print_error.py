from colorama import Fore

from .constant import CANCELLED_INPUT, GenericMessages
from .countdown import countdown


def print_error(
    error: Exception,
    generic_messages: GenericMessages,
):
    """
    Prints the error message and invokes a countdown using generic messages.
    Args:
        error: The exception instance representing the error that occurred.
        generic_messages: An instance of GenericMessages used for providing messages
            during the countdown process.
    """
    print(f"\n{Fore.RED}An error occurred : {Fore.RESET}")
    print(f"{Fore.RED}{error}{Fore.RESET}")
    countdown(generic_messages)


def get_menus_keys(menus: list | dict) -> list[str] | None:
    """
    Retrieves the keys or indices of menu items depending on the input type.
    """
    if isinstance(menus, dict):
        return list(menus.keys())
    if isinstance(menus, list):
        return [str(i + 1) for i in range(len(menus))]
    return None


def print_invalid_option(
    menus_keys: list[str],
    optional_choices: bool = False,
    generic_messages: GenericMessages = GenericMessages.PREVIOUS_MENU_RETURN,
):
    """
    Prints a message to indicate an invalid option has been chosen and provides clarity
    on valid user inputs, with custom options for optional choices and accompanying messages.

    Args:
        menus_keys (list[str]): A list containing the valid menu keys/options that the
            user can choose from.
        optional_choices (bool, optional): Indicates whether the optional "Enter" or
            "cancel" choices are enabled. Defaults to False.
        generic_messages (GenericMessages, optional): A predefined message to use with
            the countdown prompt. Defaults to GenericMessages.PREVIOUS_MENU_RETURN.
    """
    print(
        f"{Fore.RED}Invalid option, please choose between: "
        f"{Fore.LIGHTYELLOW_EX}{", ".join(menus_keys)}{Fore.RED}"
        f"{f", or press '{Fore.LIGHTYELLOW_EX}Enter{Fore.RED}' or '"
           f"{Fore.LIGHTYELLOW_EX}{CANCELLED_INPUT}{Fore.RED}' to exit" if optional_choices else ""}.{Fore.RESET}"
    )
    countdown(generic_messages)
