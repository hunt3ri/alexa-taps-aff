import os

import requests


class OpenWeatherService:

    def __init__(self):
        self.api_key = os.getenv('OPEN_WEATHER_KEY', None)  # Key used to access the Open Weather API

        if self.api_key is None:
            raise ValueError('OPEN_WEATHER_KEY environment variable not set')

    def get_temp_for_place(self, place_name: str) -> str:
        """ Lookup temp for supplied place """

        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={place_name}&appid={self.api_key}&units=metric'
        response = requests.get(weather_url)

        if response.status_code == 200:
            weather_json = response.json()

        return 'test'
