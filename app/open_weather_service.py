import os

import requests

from requests import Response

from app.weather_models import CurrentWeather, MainWeatherData
from app.utils import NotFound, TapsAffError

TAPS_AFF_THRESHOLD = 20


class OpenWeatherService:

    def __init__(self, place_name: str):
        self.api_key = os.getenv('OPEN_WEATHER_KEY', None)  # Key used to access the Open Weather API

        if self.api_key is None:
            raise ValueError('OPEN_WEATHER_KEY environment variable not set')

        self.place_name = place_name
        self.taps_aff_threshold = TAPS_AFF_THRESHOLD

    def get_taps_aff_forecast(self) -> str:
        """ Build forecast phrase for Alexa """
        try:
            current_weather = self._get_current_weather_data()
            return self._is_it_taps_aff(current_weather.main)
        except NotFound:
            return f"Sorry, pal I cannay find any forecast for {self.place_name}"
        except TapsAffError:
            return f"Sorry captain problem with the engine. A cannay change the laws of physics. Try again in a couple of minutes"

    def _is_it_taps_aff(self, main_weather_data: MainWeatherData) -> str:
        """ Builds appropriate phrase for app """
        self.temp = round(main_weather_data.temp, 1)

        if ".0" in "{:.1f}".format(self.temp):
            self.temp = int(self.temp)

        if self.temp >= self.taps_aff_threshold:
            return f'<speak><emphasis level="strong">YAS.</emphasis> It\'s taps aff in {self.place_name}. It\'s pure roasting at {self.temp} degrees</speak>'
        else:
            return f'<speak><emphasis level="strong">Gnaw mate.</emphasis> It\'s taps own in {self.place_name}. It\'s only {self.temp} degrees</speak>'

    def _get_current_weather_data(self) -> CurrentWeather:
        """ Calls weather service and parses response ready to return to user """
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={self.place_name}&appid={self.api_key}&units=metric'
        response = self._make_api_call(weather_url)

        if response.status_code == 200:
            return CurrentWeather(response.json(), strict=False)
        elif response.status_code == 404:
            raise NotFound(f'Nothing found for {self.place_name}')
        else:
            raise TapsAffError('Error with api')

    def _make_api_call(self, api_url) -> Response:
        """ Helper function to call API, useful for unit testing """
        return requests.get(api_url)
