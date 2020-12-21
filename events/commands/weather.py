import requests

from events.commands.commands import ChatCommand


class WeatherEvent(ChatCommand):

    def __init__(self, context) -> None:
        super().__init__(context)

    def get_answer(self) -> str:
        city = self.EVENT.split(' ')[1]
        return '{author}, the weather in {city} is {weather}!'.format(city=city,
                                                                      weather=self.execute_command(city),
                                                                      author='{author}')

    def execute_command(self, city):
        url = f'http://wttr.in/{city}'
        weather_parameters = {
            'format': 2,
            'M': ''
        }
        try:
            response = requests.get(url, params=weather_parameters)
        except requests.ConnectionError:
            return '<connection error>'
        if response.status_code == 200:
            return response.text.strip()
        else:
            return '<weather server connection error>'
