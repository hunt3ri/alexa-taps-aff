from marshmallow import Schema, fields, EXCLUDE


class MainWeatherData(Schema):
    """ Models main weather response from OpenWeather Current Weather API """
    temp = fields.Float()


class CurrentWeather(Schema):
    """ Models OpenWeather Current Weather API """
    main = fields.Nested(MainWeatherData, unknown=EXCLUDE)

    class Meta:
        unknown = EXCLUDE  # Only representing the model partially so ensure we exclude unknown params
