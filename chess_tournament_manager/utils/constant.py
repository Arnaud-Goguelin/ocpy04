from enum import Enum

MAX_NUMBER_OF_ROUNDS = 4
CANCELLED_INPUT = "Q"
VALIDATION_INPUT = "Y"
INVALIDATION_INPUT = "N"


class DataFilesNames(str, Enum):
    PLAYERS_FILE = "players.json"
    TOURNAMENTS_FILE = "tournaments.json"


class SolveMatchChoices(str, Enum):
    PLAYER_1 = "1"
    PLAYER_2 = "2"
    DRAW = "3"


class GenericMessages(str, Enum):
    PLAYER_MENU_RETURN = "Go back to Player menu in ... "
    TOURNAMENT_MENU_RETURN = "Go back to Tournament menu in ... "
    MAIN_MENU_RETURN = "Go back to Main menu in ... "
    PREVIOUS_MENU_RETURN = "Go back to previous menu in ... "
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
