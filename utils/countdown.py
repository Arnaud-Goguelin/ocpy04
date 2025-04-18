import time


def countdown(menu_name: str):
    for i in range(3, -1, -1):
        print(f"\rGo back to {menu_name} menu in... {i}", end="", flush=True)
        time.sleep(1)
    print("\n")
    return None
