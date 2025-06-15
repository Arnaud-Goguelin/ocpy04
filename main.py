from controllers import MainController
from models import Data


class Application:

    def __init__(self):

        self.data = Data()
        # TODO why twice data.load?
        self.data.load()
        self.controller = MainController(self.data)

    def run(self):

        # TODO delete this ligne, it is already calles in save and load methods
        self.data.validate_directory_and_files()
        # TODO why twice data.load?
        self.data.load()

        while True:
            self.controller.handle_main_menu()


if __name__ == "__main__":
    app = Application()
    app.run()
