from enum import Enum

MAX_NUMBER_OF_ROUNDS = 4
CANCELLED_INPUT = "q"


class GenericMessages(str, Enum):
    PLAYER_MENU_RETURN = "Go back to Player menu in ... "
    TOURNAMENT_MENU_RETURN = "Go back to Tournament menu in ... "
    MAIN_MENU_RETURN = "Go back to Main menu in ... "
    PLAYER_LIST = "Player list display in ... "
    EXIT_MESSAGE = r"""
            Thanks you and goodbye.
                    ,....,
                  ,::::::<
                 ,::/^\"``.
                ,::/, `   e`.
               ,::; |        '.
               ,::|  \___,-.  c)
               ;::|     \   '-'
               ;::|      \
               ;::|   _.=`\
               `;:|.=` _.=`\
                 '|_.=`   __\
                 `\_..==`` /
                  .'.___.-'.
                 /          \
                ('--......--')
                /'--......--'\
                `"--......--"
            Knight by Joan G. Stark
    """
