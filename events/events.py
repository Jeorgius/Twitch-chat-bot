import random
from abc import abstractmethod, ABC
from pathlib import Path
import os

import simplejson

from events.files.predictions import predictions

current_path = os.path.dirname(__file__)
data_folder = Path(current_path + "/files/")


class Event(ABC):
    CONTEXT = {}
    EVENT = ''
    ANSWER = ''

    def __init__(self, context) -> None:
        self.CONTEXT = context
        self.EVENT = context.content

    @abstractmethod
    def get_answer(self) -> str:
        pass


class PersonalEvent(Event):
    def get_answer(self) -> str:
        with open(data_folder / "answers.json", "r", encoding="utf-8") as file:
            answers = simplejson.load(file)
        for answer in answers:
            if answer['question'].lower() in self.EVENT.lower():
                return answers['answer']
        return ''


class CommonEvent(Event):
    def get_answer(self) -> str:
        with open(data_folder / "chat-events.json", "r", encoding="utf-8") as file:
            events = simplejson.load(file)
        for event in events:
            if event['event'].lower() in self.EVENT.lower():
                return event['answer']
        return ''


class ShowCommandInfo(Event):
    def get_answer(self) -> str:
        with open(data_folder / "commands.json", "r", encoding="utf-8") as file:
            commands = simplejson.load(file)
        for command in commands:
            if command['name'].lower() in self.EVENT.lower():
                return command['value']
        return ''


class AvailableCommands(Event):
    def get_answer(self) -> str:
        with open(data_folder / "commands.json", "r", encoding="utf-8") as file:
            commands = simplejson.load(file)
        answer = []
        for command in commands:
            answer.append(command['name'])
        if len(answer) == 0:
            return 'No commands available'
        return 'Available commands: ' + ' '.join(answer)

class EightBall(Event):
    def get_answer(self) -> str:
        return f"@{self.CONTEXT.author.name},  {random.choice(predictions)}"
