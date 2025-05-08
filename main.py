from controllers import MainController
from models import Player, Tournament
from utils import countdown, GenericMessages


class Data:
    def __init__(self):
        self.players = [
            Player(first_name="John", last_name="Johnson", birthdate="03-03-1973", chess_id="EF23456"),
            Player(first_name="Mary", last_name="Marydotter", birthdate="04-04-1974", chess_id="GH78910"),
            Player(first_name="Alice", last_name="Alicedotter", birthdate="02-02-1972", chess_id="CD67891"),
            Player(first_name="Bob", last_name="Bobson", birthdate="01-01-1970", chess_id="AB12345"),
        ]
        self.tournaments = [
            Tournament(
                name="Tournament Test",
                location=("some where..."),
                description=("...over the seas"),
                players={player for player in self.players},
            )
        ]

    def save(self):
        pass

    def load(self):
        pass

    # TODO from a JSON file complete attributes of Data class


class Application:

    def __init__(self):

        self.data = Data()
        self.data.load()
        self.controller = MainController(self.data)

    def run(self):
        while True:
            try:
                self.controller.handle_main_menu()
            except Exception as error:
                print("\nAn error occurred : ")
                print(error)
                countdown(GenericMessages.MAIN_MENU_RETURN.value)


if __name__ == "__main__":
    app = Application()
    app.run()
