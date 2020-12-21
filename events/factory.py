from twitchio import Context

from events.commands.duel import DuelEvent
from events.editor import CommandEditor
from events.commands.weather import WeatherEvent
from events.events import Event, PersonalEvent, CommonEvent, ShowCommandInfo, AvailableCommands, EightBall


class EventFactory:
    bot_name = ''

    def __init__(self, bot_name):
        self.bot_name = bot_name

    def produce_event(self, context: Context) -> Event:
        msg_lower = context.content.lower()
        if self.bot_name in msg_lower:
            return PersonalEvent(context)
        elif '!weather' in msg_lower:
            return WeatherEvent(context)
        elif '!duel' in msg_lower:
            return DuelEvent(context)
        elif '!8ball' in msg_lower:
            return EightBall(context)
        elif '!commands' in msg_lower:
            return AvailableCommands(context)
        elif '!command' in msg_lower and context.author.is_mod:
            return CommandEditor(context)
        elif '!' in msg_lower:
            return ShowCommandInfo(context)
        return CommonEvent(context)
