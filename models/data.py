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
        selected_file = os.path.join(self.data_folder, file_name)

        with open(selected_file, "w") as file:
            json.dump(instance_to_save.to_dict(), file)

        return None

    # TODO: when saving the list of players for a tournament, only save the player's ID
    #  create to_dict and from_dict methods for each model
    #  open a JSON file with the 'with' keyword
    #  write each model instance using the to_dict method
    #  close the JSON file
    #  we can have one file per data model

    def load(self):
        pass
        # TODO from a JSON file complete attributes of Data class
        # depuis le ficheir json, créer une isntance de chaque modèle pour chaque dict dans le fichier
