import os
import simplejson
import copy
from pathlib import Path
from random import randint

from events.commands.game import Game

duel_commands = [
    "accept",
    "reject",
    "shoot",
    "surrender",
    "help"
]

damage = {
    "head": 60,
    "torso": 35,
    "stomach": 35,
    "legs": 20,
    "hands": 20
}

current_path = os.path.dirname(__file__)
data_folder = Path(current_path + "/files/")


class DuelEvent(Game):

    def __init__(self, context) -> None:
        self.GAME_NAME = 'duel'
        super().__init__(context)
        self.execute_command(self.EVENT)

    def get_answer(self) -> str:
        return self.ANSWER

    def execute_command(self, event):
        commands = event.split(' ')
        game = self.find_game(self.GAME_NAME)
        action = commands[1].lower()
        if commands[1][:1] == '@' and game is None:
            self.challenge_chatter(commands)
        elif commands[1][:1] == '@' and game is not None:
            self.ANSWER = f"@{self.CONTEXT.author.name}, there's still unfinished duel."
        elif action == 'help':
            self.help(game)
        elif action == 'reject' or action == 'surrender':
            self.finish_challenge(game, commands)
        elif action == 'accept':
            self.accept_challenge(game)
        elif action == 'shoot':
            self.shoot(commands, game)

    def challenge_chatter(self, commands):
        duel_user_name = ''
        challenged = commands[1][1:]
        for user in self.CONTEXT.channel.chatters:
            if user.name == challenged:
                duel_user_name = user.name
            if challenged == self.CONTEXT.channel.name:
                duel_user_name = self.CONTEXT.channel.name
        if duel_user_name != '':
            self.ANSWER = f'@{challenged}, you have been challenged to a duel. Type accept or reject'
            duel = {
                "game": "duel",
                "actors": [
                    {
                        "name": self.CONTEXT.author.name,
                        "accepted": True,
                        "hp": 100,
                        "shoots": False,
                        "accuracy": {
                            "head": 30,
                            "torso": 65,
                            "stomach": 65,
                            "legs": 45,
                            "hands": 45
                        }

                    },
                    {
                        "name": challenged,
                        "accepted": False,
                        "hp": 100,
                        "shoots": True,
                        "accuracy": {
                            "head": 30,
                            "torso": 65,
                            "stomach": 65,
                            "legs": 45,
                            "hands": 45
                        }

                    }
                ]
            }
            self.SAVED_CONTEXT.append(duel)
            with open(data_folder / "context.json", "w", encoding="utf-8") as file:
                simplejson.dump(self.SAVED_CONTEXT, file, indent=4, sort_keys=True)
        else:
            self.ANSWER = f'@{self.CONTEXT.author.name}, no such user with nickname {challenged}'

    def get_opponent(self, game):
        if game['actors'][0]['name'] != self.CONTEXT.author.name:
            return game['actors'][0]
        else:
            return game['actors'][1]

    def get_player(self, game):
        if game['actors'][0]['name'] == self.CONTEXT.author.name:
            return game['actors'][0]
        else:
            return game['actors'][1]

    def finish_challenge(self, old_game, commands):
        self.delete_game(old_game)
        with open(data_folder / "context.json", "w", encoding="utf-8") as file:
            simplejson.dump(self.SAVED_CONTEXT, file, indent=4, sort_keys=True)

        last_command = commands[1].lower()

        if last_command == 'reject':
            self.ANSWER = f'@{self.CONTEXT.author.name} cancelled duel with @{self.get_opponent(old_game)["name"]}'
        elif last_command == 'surrender':
            self.ANSWER = f'@{self.CONTEXT.author.name} has surrendered against @{self.get_opponent(old_game)["name"]}'
        elif last_command == 'shoot':
            self.ANSWER += f"@{self.get_opponent(old_game)['name']}, you're dead. DED! KEKW Duel is over."

    def shoot(self, commands, game):
        target = commands[2].lower()
        player = self.get_player(game)
        opponent = self.get_opponent(game)

        if target not in damage:
            self.ANSWER = f'@{self.CONTEXT.author.name}, no such target - {target}'
            return
        if not player['shoots'] or not player['accepted'] or not opponent['accepted']:
            self.ANSWER = f'@{self.CONTEXT.author.name}, wait for your turn or the duel to start'
            return

        is_hit = randint(0, 100) <= player['accuracy'][target]
        if is_hit:
            damage_dealt = damage[target] - randint(-5, 5)
            opponent['hp'] -= damage_dealt
            self.reduce_accuracy(target, opponent)
            self.ANSWER = f"@{player['name']}, you hit {opponent['name']} and deal {damage_dealt}hp damage. KEKWait "
        else:
            self.ANSWER = f"@{player['name']}, you missed KEKW "
        if opponent['hp'] > 0:
            self.ANSWER += (f"@{opponent['name']}, you have {opponent['hp']}hp."
                            f'Type !duel shoot ... (choose target). Your accuracy is: ')
            for target in opponent['accuracy']:
                self.ANSWER += f"[{target}={opponent['accuracy'][target]}] "
            player['shoots'] = False
            opponent['shoots'] = True
            game['actors'] = [player, opponent]
            self.save_game_changes(game)
        else:
            self.finish_challenge(game, commands)

    @staticmethod
    def reduce_accuracy(target, opponent):
        if target in ['head', 'torso', 'stomach']:
            for t in opponent['accuracy']:
                opponent['accuracy'][t] -= randint(0, 7)
        else:
            for t in opponent['accuracy']:
                opponent['accuracy'][t] -= randint(5, 15)

    def accept_challenge(self, game):
        player = self.get_player(game)
        player['accepted'] = True
        game['actors'] = [player, self.get_opponent(game)]
        self.save_game_changes(game)
        self.ANSWER = (f"@{player['name']}, challenge accepted. Type !duel shoot ... and choose your target."
                       f"Your accuracy is: ")
        for target in player['accuracy']:
            self.ANSWER += f"[{target}={player['accuracy'][target]}] "

    def help(self, game):
        if game is None:
            self.ANSWER = f"@{self.CONTEXT.author.name}, there's no duel for you."
            return
        player = self.get_player(game)
        opponent = self.get_opponent(game)

        if not player['accepted'] or not opponent['accepted']:
            self.ANSWER = f"@{self.CONTEXT.author.name}, duel was not accepted by one of the players."
            return
        statement = [
            f"@{player['name']}, your opponent is {opponent['name']}",
            "Available commands: " + ", ".join(duel_commands)
        ]

        if player['shoots']:
            statement.append("It's your turn to shoot")
        else:
            statement.append("It's not your turn to shoot")

        accuracy = ''
        for target in player['accuracy']:
            accuracy += f"[{target}={player['accuracy'][target]}] "
        statement.append("Accuracy: " + accuracy)
        self.ANSWER = '. '.join(statement)
