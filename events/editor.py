import os
from pathlib import Path

import simplejson

from events.commands.commands import ChatCommand

current_path = os.path.dirname(__file__)
data_folder = Path(current_path + "/files/")


class CommandEditor(ChatCommand):
    SAVED_CONTEXT = []

    def __init__(self, context) -> None:
        super().__init__(context)
        with open(data_folder / "commands.json", "r", encoding="utf-8") as file:
            self.SAVED_CONTEXT = simplejson.load(file)
        self.execute_command(self.EVENT)

    def get_answer(self) -> str:
        return self.ANSWER

    def execute_command(self, event):
        commands = event.split(' ')
        action = commands[1].lower()
        if action == 'add':
            self.add(commands)
        elif action == 'remove' or action == 'delete':
            self.delete(commands)
        elif action == 'edit':
            self.edit(commands)
        elif action == 'help':
            self.help()
        else:
            self.ANSWER = f"@{self.CONTEXT.author.name}, no known action specified"

    def add(self, commands):
        command_to_add = commands[2]
        if self.find_command(command_to_add.lower()) is not None:
            self.ANSWER = f"@{self.CONTEXT.author.name}, command {command_to_add} already exists."
            return
        self.SAVED_CONTEXT.append({
            "name": command_to_add,
            "value": " ".join(commands[3:])
        })
        self.ANSWER = f"@{self.CONTEXT.author.name}, command {command_to_add} saved."
        self.save_context()

    def delete(self, commands):
        command_to_delete = commands[2]
        if self.find_command(command_to_delete.lower()) is None:
            self.ANSWER = f"@{self.CONTEXT.author.name}, command {command_to_delete} doesn't exist."
            return
        self.delete_command(command_to_delete)
        self.save_context()
        self.ANSWER = f"@{self.CONTEXT.author.name}, command {command_to_delete} deleted."

    def edit(self, commands):
        command_mentioned = commands[2]
        command_to_edit = self.find_command(command_mentioned.lower())
        if command_to_edit is None:
            self.ANSWER = f"@{self.CONTEXT.author.name}, command {command_mentioned} doesn't exist."
            return
        command_to_edit['value'] = ' '.join(commands[3:])
        self.save_changes(command_to_edit)
        self.ANSWER = f"@{self.CONTEXT.author.name}, command {command_to_edit['name']} edited."

    def help(self):
        self.ANSWER = f"@{self.CONTEXT.author.name}, type !command action <!command_name> <value> . " \
            f"Example: !command add !kek haha KEKW"

    def find_command(self, command_to_find):
        for command in self.SAVED_CONTEXT:
            if command['name'].lower() == command_to_find:
                return command

    def save_changes(self, command_to_save):
        self.delete_command(command_to_save['name'])
        self.SAVED_CONTEXT.append(command_to_save)
        self.save_context()

    def delete_command(self, command_to_delete: str):
        for command in self.SAVED_CONTEXT:
            if command_to_delete == command['name']:
                self.SAVED_CONTEXT.remove(command)

    def save_context(self):
        with open(data_folder / "commands.json", "w", encoding="utf-8") as file:
            simplejson.dump(self.SAVED_CONTEXT, file)
