import time


def countdown(message: str):
    for i in range(3, -1, -1):
        print(f"\r{message}{i}", end="", flush=True)
        time.sleep(1)
    print("\n")
    return None
