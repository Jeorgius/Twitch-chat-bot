from abc import abstractmethod

from events.events import Event


class ChatCommand(Event):

    @abstractmethod
    def execute_command(self, event):
        pass
