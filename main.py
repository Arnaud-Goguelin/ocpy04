from controllers import MainController
from models import Player, Tournament


class Data:
    def __init__(self):
        self.players = [
            Player(first_name="John", last_name="Johnson", birthdate="03-03-1973", chess_id="EF23456"),
            Player(first_name="Mary", last_name="Marydotter", birthdate="04-04-1974", chess_id="GH78910"),
            Player(first_name="Alice", last_name="Alicedotter", birthdate="02-02-1972", chess_id="CD67891"),
            Player(first_name="Bob", last_name="Bobson", birthdate="01-01-1970", chess_id="AB12345"),
            Player(first_name="Jane", last_name="Janedotter", birthdate="05-05-1975", chess_id="AB12345"),
            Player(first_name="Jill", last_name="Jilldotter", birthdate="06-06-1976", chess_id="MN34567"),
            Player(first_name="Peter", last_name="Peterson", birthdate="07-07-1977", chess_id="IJ34567"),
            Player(first_name="Sarah", last_name="Sarahdotter", birthdate="08-08-1978", chess_id="KL89012")
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
            self.controller.handle_main_menu()


if __name__ == "__main__":
    app = Application()
    app.run()
