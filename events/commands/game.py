import os
import simplejson
from pathlib import Path
from events.filepaths import context_paths
from events.commands.commands import ChatCommand

current_path = os.path.dirname(__file__)
data_folder = Path(current_path + "/files/")


class Game(ChatCommand):
    SAVED_CONTEXT = []
    GAME_NAME = ''

    def __init__(self, context, game_name: str) -> None:
        super().__init__(context)
        self.GAME_NAME = game_name
        with open(context_paths[self.GAME_NAME], "r", encoding="utf-8") as file:
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
        self.save_into_file()

    def delete_game(self, game):
        for available_game in self.SAVED_CONTEXT:
            if game['actors'][0]['name'] == available_game['actors'][0]['name']:
                self.SAVED_CONTEXT.remove(available_game)

    def save_into_file(self):
        with open(context_paths[self.GAME_NAME], "w", encoding="utf-8") as file:
            simplejson.dump(self.SAVED_CONTEXT, file)
