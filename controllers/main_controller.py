# need to import others controllers with an absolut path to avoid the circular import issue.
from controllers.player.player_controller import PlayerController
from utils.error_handler import error_handler
from views import MainMenuView


class MainController:
    def __init__(self):
        self.view = MainMenuView()

    def handle_main_menu(self):
        while True:
            self.view.display()
            result = self.process_menu_choice()
            if result == "continue":
                continue
            elif result == "exit":
                break

    @error_handler
    def process_menu_choice(self):
        choice = input("Choose an option : ")
        if choice == "1":
            player_controller = PlayerController()
            player_controller.handle_player_main_menu()
        elif choice == "2":
            pass
        elif choice == "3":
            print(r"""
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
    """)
            return "exit"
        else:
            raise ValueError("Invalid option, please choose between 1, 2 or 3.")
