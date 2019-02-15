import json
import os
import pytest

from unittest.mock import patch

from app.open_weather_service import OpenWeatherService, Response, NotFound, TapsAffError, MainWeatherData


class TestOpenWeatherService:

    def test_get_weather_service_returns_temp(self):
        # Arrange
        weather_service = OpenWeatherService(place_name='Stirling')

        # Act
        phrase = weather_service.get_taps_aff_forecast()

        if weather_service.temp >= weather_service.taps_aff_threshold:
            assert "taps aff" in phrase
        else:
            assert "taps own" in phrase
