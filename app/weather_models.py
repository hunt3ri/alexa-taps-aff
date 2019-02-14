from schematics import Model
from schematics.types import FloatType, StringType
from schematics.types.compound import ModelType


class MainWeatherData(Model):
    """ Models main weather response from OpenWeather Current Weather API """
    temp = FloatType()


class CurrentWeather(Model):
    """ Models OpenWeather Current Weather API """
    main = ModelType(MainWeatherData)
    name = StringType()
