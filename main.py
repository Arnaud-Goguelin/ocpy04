from controllers import MainController
from models import Data


class Application:

    def __init__(self):

        self.data = Data()
        self.controller = MainController(self.data)

        self.data.load()

    def run(self):

        while True:
            self.controller.handle_main_menu()


if __name__ == "__main__":
    app = Application()
    app.run()
