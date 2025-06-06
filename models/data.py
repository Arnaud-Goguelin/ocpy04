import json
import os

from colorama import Fore

from models.player import Player
from models.tournament import Tournament
from utils import DataFilesNames


class Data:
    def __init__(self):
        self.players = []
        self.tournaments = []
        self.data_folder = "data"

    # TODO be sure data folder exist on remote repository and be sure file are created if they do not exist
    def validate_directory(self):
        os.makedirs(self.data_folder, exist_ok=True)

    def save(self, file_name: DataFilesNames) -> None:
        try:
            self.validate_directory()
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

        self.validate_directory()

        file_mappings = {
            DataFilesNames.PLAYERS_FILE: Player,
            DataFilesNames.TOURNAMENTS_FILE: Tournament,
        }

        for file_name, model in file_mappings.items():
            try:
                file_path = os.path.join(self.data_folder, file_name.value)

                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        instances = [model.from_dict(item_dict) for item_dict in data]
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
                    file.write("")
            except (json.JSONDecodeError, TypeError) as error:
                raise Exception(f"Error erasing in {file_name.value}: {error}")
        print(f"{Fore.MAGENTA}--- Data erased. ---{Fore.RESET}")
