import json
import os
import pytest

from unittest.mock import patch

from app.open_weather_service import OpenWeatherService, Response, NotFound, TapsAffError, MainWeatherData


class TestOpenWeatherService:

    @patch.object(OpenWeatherService, '_make_api_call')
    def test_not_found_raised_if_place_not_found(self, mock_api_call):
        # Arrange
        stub_api_response = Response()
        stub_api_response.status_code = 404
        mock_api_call.return_value = stub_api_response

        # Act / Assert
        with pytest.raises(NotFound):
            OpenWeatherService(place_name='xxx')._get_current_weather_data()

    @patch.object(OpenWeatherService, '_make_api_call')
    def test_taps_aff_error_raised_if_unknown_exception_found(self, mock_api_call):
        # Arrange
        stub_api_response = Response()
        stub_api_response.status_code = 500
        mock_api_call.return_value = stub_api_response

        # Act / Assert
        with pytest.raises(TapsAffError):
            OpenWeatherService(place_name='xxx')._get_current_weather_data()

    @patch.object(OpenWeatherService, '_make_api_call')
    def test_temp_returned_if_request_valid(self, mock_api_call):
        # Arrange
        api_response = json.dumps(self.get_canned_json('current_weather_api_response.json'))

        stub_api_response = Response()
        stub_api_response.status_code = 200
        stub_api_response._content = api_response.encode('utf-8')
        mock_api_call.return_value = stub_api_response

        # Act
        current_weather = OpenWeatherService(place_name='Stirling')._get_current_weather_data()

        # Assert
        assert current_weather.main['temp'] == 6.5

    def test_its_taps_aff_if_over_threshold(self):
        # Arrange
        main_weather = MainWeatherData()
        main_weather.temp = 30

        # Act
        phrase = OpenWeatherService(place_name='Stirling')._is_it_taps_aff(main_weather)

        # Assert
        assert "taps aff" in phrase
        assert "Stirling" in phrase
        assert "30" in phrase

    def test_its_taps_own_if_over_threshold(self):
        # Arrange
        main_weather = MainWeatherData()
        main_weather.temp = 5

        # Act
        phrase = OpenWeatherService(place_name='Stirling')._is_it_taps_aff(main_weather)

        # Assert
        assert "taps own" in phrase
        assert "Stirling" in phrase
        assert "5" in phrase

    def test_float_rounding_trims_point_zero(self):
        # Arrange
        main_weather = MainWeatherData()
        main_weather.temp = 9.97

        # Act
        phrase = OpenWeatherService(place_name='Stirling')._is_it_taps_aff(main_weather)

        # Assert
        assert "10" in phrase

    def test_float_rounding_does_not_trip_single_decimaal_point(self):
        # Arrange
        main_weather = MainWeatherData()
        main_weather.temp = 10.5

        # Act
        phrase = OpenWeatherService(place_name='Stirling')._is_it_taps_aff(main_weather)

        # Assert
        assert "10.5" in phrase

    def test_float_rounding_does_not_works_for_multiple_decimal_points(self):
        # Arrange
        main_weather = MainWeatherData()
        main_weather.temp = 10.55

        # Act
        phrase = OpenWeatherService(place_name='Stirling')._is_it_taps_aff(main_weather)

        # Assert
        assert "10.6" in phrase

    def get_canned_json(self, file_name: str):
        """ Read canned api response from file """
        location = os.path.join(os.path.dirname(__file__), 'test_files', file_name)

        try:
            with open(location, 'r') as api_file:
                data = json.load(api_file)
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f'{file_name} not found')
