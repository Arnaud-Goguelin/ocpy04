from controllers import MainController
from models import Data


class Application:

    def __init__(self):

        self.data = Data()
        self.data.load()
        self.controller = MainController(self.data)

    def run(self):

        # tournament = self.data.tournaments[0]
        # test = tournament.to_dict()
        # print(test)
        self.data.validate_directory()

        while True:
            self.controller.handle_main_menu()


if __name__ == "__main__":
    app = Application()
    app.run()
