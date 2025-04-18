from controllers import MainController
from utils import countdown


class Data:
    def __init__(self):
        # TODO begin with players instances
        self.players = []

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
                countdown(menu_name="main")


if __name__ == "__main__":
    app = Application()
    app.run()
