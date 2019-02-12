from app.weather_service import WeatherService


class TestWeatherService:

    def test_get_weather_service_returns_temp(self):
        # Act
        temp = WeatherService().get_temp_for_place('Glasgow')

        assert temp == 'test', "Temp should be returned"
