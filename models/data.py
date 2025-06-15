import json
import os

from colorama import Fore

from models.player import Player
from models.tournament import Tournament
from utils import DataFilesNames


class Data:
    def __init__(self):
        self.players = set()
        self.tournaments = set()
        self.data_folder = "data"

    def validate_directory_and_files(self):
        # create the 'data' folder if it does not exist
        os.makedirs(self.data_folder, exist_ok=True)

        # create files if they do not exist
        for file_name in DataFilesNames:
            file_path = os.path.join(self.data_folder, file_name.value)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump([], file, indent=4)

    def save(self, file_name: DataFilesNames) -> None:
        self.validate_directory_and_files()
        try:
            selected_file = os.path.join(self.data_folder, file_name)

            # with the id we could find in all_data
            # the instance with the same id as instance_to_save
            # and just update it

            if file_name == DataFilesNames.PLAYERS_FILE:
                data = [player.to_dict() for player in self.players]

            if file_name == DataFilesNames.TOURNAMENTS_FILE:
                data = [tournament.to_dict() for tournament in self.tournaments]

            with open(selected_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            return None

        except (json.JSONDecodeError, TypeError) as error:
            raise Exception(f"Error saving in {file_name.value}: {error}")

    def load(self) -> None:
        """
        Loads data from predefined files into their respective models. This method first validates
        the directory and files, then processes `Players` and `Tournaments` data in this order.
        The data is read from JSON files, with error handling to manage decoding issues or empty files.
        The loaded data is converted into model instances and stored in the object.

        :raises Exception: If there is an error during loading data from JSON.

        :return: None
        """

        self.validate_directory_and_files()

        # use a list to keep an order, it is necessary to load Players before Tournaments
        # as Tournaments only store Players ids, we need to get Player instance from self.players
        # thanks to ids in Tournaments
        # TODO: check order_dict
        file_mappings = [
            (DataFilesNames.PLAYERS_FILE, Player),
            (DataFilesNames.TOURNAMENTS_FILE, Tournament),
        ]

        for file_name, model in file_mappings:
            try:
                file_path = os.path.join(self.data_folder, file_name.value)

                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as file:
                        # load data here and ensure we have at least an empty list
                        data = []
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            if isinstance(data, list) and len(data) == 0:
                                pass

                        if not data:
                            print(
                                f"{Fore.MAGENTA}--- Chess App started with empty data in {file_name.value}. ---{Fore.RESET}"
                            )
                        else:
                            instances = set(model.from_dict(item_dict, self) for item_dict in data)
                            setattr(self, f"{model.__name__.lower()}s", instances)

            except (json.JSONDecodeError, TypeError) as error:
                raise Exception(f"Error loading in {file_name.value}: {error}")

        return None

    # TODO: delete once dev is finished
    def erase(self) -> None:
        for file_name in DataFilesNames:
            try:
                selected_file = os.path.join(self.data_folder, file_name)
                with open(selected_file, "w", encoding="utf-8") as file:
                    file.write("[]")
            except (json.JSONDecodeError, TypeError) as error:
                raise Exception(f"Error erasing in {file_name.value}: {error}")
        print(f"{Fore.MAGENTA}--- Data erased. ---{Fore.RESET}")
