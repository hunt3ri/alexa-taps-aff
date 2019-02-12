from app.open_weather_service import OpenWeatherService


class TestOpenWeatherService:

    def test_get_weather_service_returns_temp(self):
        # Act
        temp = OpenWeatherService().get_temp_for_place('Glasgow')

        assert temp == 'test', "Temp should be returned"
