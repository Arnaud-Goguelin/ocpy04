import json
import os

from models.player import Player
from models.tournament import Tournament
from utils import DataFilesNames


class Data:
    def __init__(self):
        self.players = [
            Player(first_name="John", last_name="Johnson", birthdate="03-03-1973", chess_id="EF23456"),
            Player(first_name="Mary", last_name="Marydotter", birthdate="04-04-1974", chess_id="GH78910"),
            Player(first_name="Alice", last_name="Alicedotter", birthdate="02-02-1972", chess_id="CD67891"),
            Player(first_name="Bob", last_name="Bobson", birthdate="01-01-1970", chess_id="AB12345"),
            Player(first_name="Jane", last_name="Janedotter", birthdate="05-05-1975", chess_id="AB12345"),
            Player(first_name="Jill", last_name="Jilldotter", birthdate="06-06-1976", chess_id="MN34567"),
            Player(first_name="Peter", last_name="Peterson", birthdate="07-07-1977", chess_id="IJ34567"),
            Player(first_name="Sarah", last_name="Sarahdotter", birthdate="08-08-1978", chess_id="KL89012"),
        ]
        self.tournaments = [
            Tournament(
                name="Tournament Test",
                location=("some where..."),
                description=("...over the seas"),
                players={player for player in self.players},
            )
        ]
        self.data_folder = "data"

    def validate_directory(self):
        os.makedirs(self.data_folder, exist_ok=True)

    def save(self, file_name: DataFilesNames, instance_to_save: Player | Tournament) -> None:
        try:
            self.validate_directory()
            selected_file = os.path.join(self.data_folder, file_name)

            all_data = []
            if os.path.exists(selected_file) and os.path.getsize(selected_file) > 0:
                with open(selected_file, "r", encoding="utf-8") as file:
                    all_data = json.load(file)

            # with the id we could find in all_data
            # the instance with the same id as instance_to_save
            # and just update it

            all_data.append(instance_to_save.to_dict())

            with open(selected_file, "w", encoding="utf-8") as file:
                json.dump(all_data, file, indent=4)

            return None

        except (json.JSONDecodeError, TypeError) as error:
            raise Exception(f"Error saving in {file_name.value}: {error}")
        except Exception as error:
            raise Exception(f"Error saving in {file_name.value}: {error}")

    def load(self):
        pass
        # TODO from a JSON file complete attributes of Data class
        # depuis le ficheir json, créer une isntance de chaque modèle pour chaque dict dans le fichier
