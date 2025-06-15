import time

from .constant import GenericMessages


def countdown(message: GenericMessages):
    """
    Counts down from 3 to 0 with a given message prefix, displaying each number in
    a single line dynamically and pausing for one second between each decrement.

    Args:
        message (GenericMessages): A message object containing the prefix to
            display before the countdown number.
    """
    for i in range(3, -1, -1):
        print(f"\r{message.value}{i}", end="", flush=True)
        time.sleep(1)
    print("\n")
    return None
