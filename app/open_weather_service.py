import os

import requests

from requests import Response

from app.weather_models import CurrentWeather
from app.utils import NotFound, TapsAffError


class OpenWeatherService:

    def __init__(self, place_name: str):
        self.api_key = os.getenv('OPEN_WEATHER_KEY', None)  # Key used to access the Open Weather API

        # bb08b96b2a28b4a00ce434efa6521198
        if self.api_key is None:
            raise ValueError('OPEN_WEATHER_KEY environment variable not set')

        self.place_name = place_name

    def get_taps_aff_forecast(self) -> str:
        pass

    def get_temp_for_place(self) -> float:
        """ Lookup temp for supplied place """

        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={self.place_name}&appid={self.api_key}&units=metric'
        response = requests.get(weather_url)

        if response.status_code == 200:
            current_weather = CurrentWeather().loads(response.json())

            weather_json = response.json()

        return 'test'

    def _get_current_weather_data(self) -> CurrentWeather:

        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={self.place_name}&appid={self.api_key}&units=metric'
        response = self._make_api_call(weather_url)

        if response.status_code == 200:
            iain = response.json()
            bob = CurrentWeather().load(response.json())
            abi = bob['main']['temp']
            lou = abi
            #return CurrentWeather().load(response.json())
        elif response.status_code == 404:
            raise NotFound(f'Nothing found for {self.place_name}')
        else:
            raise TapsAffError('Error with api')

    def _make_api_call(self, api_url) -> Response:
        """ Helper function to call API, useful for unit testing """
        return requests.get(api_url)
