from get_adelphi_info import AdelphiInfo
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import json


obj1 = AdelphiInfo()  # Creates the JSON file
sb = SkillBuilder()   # Creates SkillBuilder object


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
class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool

        # Checks to see if the intent name is 'HelloWorldIntent' returns true if it is
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        filename = "data/adelphi_calendar.json"
        speech_text = "Hello World"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) \
                or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get it. Can you please say it again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


# Creates the Lambda handler
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
