import os
import simplejson
from pathlib import Path
from events.commands.commands import ChatCommand

current_path = os.path.dirname(__file__)
data_folder = Path(current_path + "/files/")


class Game(ChatCommand):
    SAVED_CONTEXT = []
    GAME_NAME = ''

    def __init__(self, context) -> None:
        super().__init__(context)
        with open(data_folder / "context.json", "r", encoding="utf-8") as file:
            self.SAVED_CONTEXT = simplejson.load(file)

    def find_game(self, game_name: str):
        author = self.CONTEXT.author.name
        for game in self.SAVED_CONTEXT:
            if game['game'] == game_name and game['actors'][0]['name'] == author or \
                    game['game'] == game_name and game['actors'][1]['name'] == author:
                return game

    def save_game_changes(self, game):
        self.delete_game(game)
        self.SAVED_CONTEXT.append(game)
        with open(data_folder / "context.json", "w", encoding="utf-8") as file:
            simplejson.dump(self.SAVED_CONTEXT, file)

    def delete_game(self, game):
        for available_game in self.SAVED_CONTEXT:
            if game['actors'][0]['name'] == available_game['actors'][0]['name']:
                self.SAVED_CONTEXT.remove(available_game)
