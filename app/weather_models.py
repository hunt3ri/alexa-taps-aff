from marshmallow import Schema, fields, EXCLUDE, post_load


class MainWeatherData(Schema):
    """ Models main weather response from OpenWeather Current Weather API """
    temp = fields.Float()


class CurrentWeatherSchema(Schema):
    """ Models OpenWeather Current Weather API """
    main = fields.Nested(MainWeatherData, unknown=EXCLUDE)
    name = fields.String()

    class Meta:
        unknown = EXCLUDE  # Only representing the model partially so ensure we exclude unknown params

    # @post_load
    # def make_current_weather(self, data):
    #     return CurrentWeatherSchema(**data)


