from controllers import MainController
from models import Data


class Application:

    def __init__(self):

        self.data = Data()
        self.data.load()
        self.controller = MainController(self.data)

    def run(self):

        self.data.validate_directory()
        self.data.load()

        while True:
            self.controller.handle_main_menu()


if __name__ == "__main__":
    app = Application()
    app.run()
