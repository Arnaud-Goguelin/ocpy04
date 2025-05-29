from colorama import Fore


def print_title(title: str):
    print()
    print(f"{Fore.GREEN}={Fore.RESET}" * len(title))
    print(title)
    print(f"{Fore.GREEN}={Fore.RESET}" * len(title))
    print()
