from .constant import CANCELLED_INPUT
from .print_error import get_menus_keys, print_invalid_option


def check_choice(choice: str, menus: list | dict) -> bool:
    """
    Checks the validity of a user's choice from a given menu. This function ensures that the input
    choice is formatted correctly, falls within the range of the available menu options, or matches
    specific optional choices. If the input is invalid, an error message is displayed, but the program
    does not terminate, allowing the user to continue interacting with the system.

    The function is designed to handle inputs in the context of a loop.

    Args:
        choice (str): The user's input choice. It may correspond to a numeric option, an
            optional choice, or an empty string for invalid cases.
        menus (list | dict): The collection of menu options. It can be a list or a dictionary
            where each element or key represents a valid menu choice.

    Returns:
        bool: Always returns True to allow the continuation of the main loop or program execution.
    """
    # as check_choice is used in loop,
    # return True to not break the loop and just display the error message
    # but let the user continue to choose his action

    if choice == "":
        # in case user press 'enter'
        return True

    if not choice.isdigit() and choice.upper() != CANCELLED_INPUT:
        print_invalid_option(menus_keys=get_menus_keys(menus), optional_choices=True)

    if choice.isdigit() and not 0 < int(choice) <= len(menus):
        print_invalid_option(menus_keys=get_menus_keys(menus), optional_choices=True)

    return True
