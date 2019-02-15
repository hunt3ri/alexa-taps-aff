# -*- coding: utf-8 -*-

# Taps Aff Alexa Skill looks up the weather for Scots
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from app.open_weather_service import OpenWeatherService

sb = SkillBuilder()

logger = logging.getLogger("taps_aff")
logger.setLevel(logging.INFO)

city_slot = "city"


def get_logger():
    """ Helper to get logger """
    if logger:
        return logger


class LaunchRequestHandler(AbstractRequestHandler):
    """ Handler for Skill Launch"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hiya!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Taps Aff", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class TapsAffIntentHandler(AbstractRequestHandler):
    """ Handler for Taps Aff Intent. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TapsAffIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots

        if city_slot in slots:
            city = slots[city_slot].value
            phrase = OpenWeatherService(place_name=city).get_taps_aff_forecast()
        else:
            phrase = "Sorry pal, you need to mention a city, when asking is it taps aff"

        handler_input.response_builder.speak(phrase).set_card(
            SimpleCard("Taps Aff", phrase)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """ Handler for Help Intent. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say is it taps aff in city of your choice"
        reprompt = "What city do you want tay check!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard("Taps Aff", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """ Single handler for Cancel and Stop Intent. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Bye for noo!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Taps Aff", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """ AMAZON.FallbackIntent is only available in en-US locale. This handler will not be triggered except
        in that locale, so it is safe to deploy on any locale. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "Sorry big man, I can't do that."
            "You can say is it taps aff in city of your choice")
        reprompt = "What city do you want tay check!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """ Handler for Session End. """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and respond with custom message. """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry pal, I didnay catch that!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


# Attach all handlers to skill builder
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TapsAffIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
