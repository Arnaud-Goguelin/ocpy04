import functools
import time


def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            print("\nAn error occurred : ")
            print(error)
            for i in range(3, -1, -1):
                print(f"\rGo back to main menu in... {i}", end="", flush=True)
                time.sleep(1)
            print("\n")

            # return "continue" to fit in handle_main_menu() method logic in MainController and display main menu
            return "continue"

    return wrapper
