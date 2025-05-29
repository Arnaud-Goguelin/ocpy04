
from .constant import CANCELLED_INPUT
from .print_error import get_menus_keys, print_invalid_option


def check_choice(choice: str, menus: list | dict ) -> bool:

    if not choice.isdigit() and choice.upper() != CANCELLED_INPUT:
        print_invalid_option(menus_keys=get_menus_keys(menus), optional_choices=True)

    if choice.isdigit() and not 0 < int(choice) <= len(menus):
        print_invalid_option(menus_keys=get_menus_keys(menus), optional_choices=True)

    # as check_choice is used in loop,
    # return True to not break the loop and just display the error message
    # but let the user continue to choose his action
    return True
