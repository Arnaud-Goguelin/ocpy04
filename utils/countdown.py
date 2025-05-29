import time

from .constant import GenericMessages


def countdown(message: GenericMessages):
    for i in range(3, -1, -1):
        print(f"\r{message.value}{i}", end="", flush=True)
        time.sleep(1)
    print("\n")
    return None
