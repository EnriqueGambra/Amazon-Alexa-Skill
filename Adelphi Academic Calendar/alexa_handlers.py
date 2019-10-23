# -*- coding: utf-8 -*-
"""Simple fact sample app."""

from datetime import date
from datetime import timedelta
import logging
import json
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from get_adelphi_info import AdelphiInfo

# =========================================================================================================================================
# TODO: The items below this comment need your attention.
# =========================================================================================================================================
SKILL_NAME = "Adelphi Calendar"
HELP_MESSAGE = "You can ask me a question about the Adelphi Calendar, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Adelphi Calendar skill can't help you with that. Please ask another question"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."

# =========================================================================================================================================
# TODO: Replace this data with your own.  You can find translations of this data at http://github.com/alexa/skill-sample-python-fact/lambda/data
# =========================================================================================================================================

# =========================================================================================================================================
# Editing anything below this line might break your skill.
# =========================================================================================================================================

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

get_json = AdelphiInfo()
filename = "/tmp/adelphi_calendar2.json"

month_num_dict = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}

num_month_dict = {
    '01': 'january',
    '02': 'february',
    '03': 'march',
    '04': 'april',
    '05': 'may',
    '06': 'june',
    '07': 'july',
    '08': 'august',
    '09': 'september',
    '10': 'october',
    '11': 'november',
    '12': 'december',
}

with open(filename) as f:
    calendar_info_dict = json.load(f)

date_event_dict = dict()

for key, value in calendar_info_dict.items():
    date_event_dict[value] = key


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)  # Returns true if it can handle this request

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        # Text that is outputted when LaunchRequest is invoked
        speech_text = "Welcome to the Adelphi Calendar skill, ask any question pertaining to the Adelphi calendar."
        # Generates the response
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


# Custom intent handler class
class AdelphiCalendarIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool

        # Checks to see if the intent name is 'HelloWorldIntent' returns true if it is
        return is_intent_name("AdelphiCalendarIntent")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response

        # data_json = get_slot_value(handler_input, value)
        # print(handler_input.request_envelope.request.intent.slots['CALENDAR_INFO'].value)
        # print(calendar_info_dict)
        utterance = handler_input.request_envelope.request.intent.slots['CALENDAR_INFO'].value
        # print("Utterance = " + utterance)
        speech_text = calendar_info_dict[utterance]
        # print("Speech text = " + speech_text)

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class DaysUntilIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool

        # Checks to see if the intent name is 'HelloWorldIntent' returns true if it is
        return is_intent_name("DaysUntilIntent")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        utterance = handler_input.request_envelope.request.intent.slots['CALENDAR_INFO'].value
        event_date = calendar_info_dict[utterance]

        if event_date.find('-') is not -1:
            month_date_list = event_date.split('-')
            month_day = month_date_list[0]
            year = event_date[len(event_date) - 4:]
            event_date = month_day + ' ' + year
        today = date.today()

        month_day_year = event_date.split(" ")

        month = month_num_dict.get(month_day_year[0])
        day = month_day_year[1]
        year = month_day_year[2]

        future = date(int(year), month, int(day))
        days_until = future - today

        if(str(days_until).find('-')) is not -1:
            speech_text = "Event already passed on " + event_date
        else:
            days_until_list = str(days_until).split(" ")
            days_left = days_until_list[0]
            speech_text = "Event is in " + str(days_left) + " days"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class NextEventIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool

        # Checks to see if the intent name is 'NextEventIntent' returns true if it is
        return is_intent_name("NextEventIntent")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        today = date.today()
        day_counter = 0
        while True:
            next_date = today + timedelta(days=day_counter)
            year_month_day = str(next_date).split("-")
            year = year_month_day[0]
            month = year_month_day[1]
            day = year_month_day[2]

            converted_date = f'{num_month_dict.get(month)} {day} {year}'
            if converted_date in date_event_dict:
                next_event = date_event_dict[converted_date]
                date_of_event = calendar_info_dict[next_event]
                speech_text = f'The next event is {next_event} and it is on {date_of_event}'
                break
            day_counter += 1

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

# Built-in Intent Handlers

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
            SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AdelphiCalendarIntentHandler())
sb.add_request_handler(DaysUntilIntentHandler())
sb.add_request_handler(NextEventIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
