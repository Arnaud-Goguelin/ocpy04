from controllers import MainController


class Application:
    def __init__(self):
        self.controller = MainController()

    def run(self):
        self.controller.handle_main_menu()


if __name__ == "__main__":
    app = Application()
    app.run()
