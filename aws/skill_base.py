from ..general import debug, Strong

from ..response import Response

class SkillBase():
    def slot_value(self, request, name):
        intent = request['intent']
        slots = intent['slots']

        if hasattr(slots, name):
            return slots[name]['value']
        else:
            return None

    def get_session_attributes(self, session):
        if hasattr(session, 'attributes'):
            return session.attributes
        else:
            return {}

    def session_value(self, session, name):
        attributes = self.get_session_attributes(session)
        if hasattr(attributes, name):
            return attributes[name]
        else:
            return None

    def get_application_id(self):
        return self.application_id

    def create_response(self):
        return Response()

    def create_error(self, status_code, message):
        response = self.create_response()
        response.status_code = 500
        response.is_error = True
        if message is not None:
            response.string_content = message

        return response

    def register_intents(self, intents):
        self.intents = intents

    def run_intent(self, intent, request, session):
        function = [y for x,y in self.intents if x == intent]
        if len(function) == 1:
            response = function[0](request, session)
        else:
            raise ValueError("Invalid intent")

        # log('response', response)

        return response

    def execute(self, request, session):
        # debug.logline("event.session.application.applicationId=" + session['application']['applicationId'])

        """
        Uncomment this if statement and populate with your skill's application ID to
        prevent someone else from configuring a skill that sends requests to this
        function.
        """
        # if (event['session']['application']['applicationId'] !=
        #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
        #     raise ValueError("Invalid Application ID")

        if hasattr(session, 'new'):
            pass

        if hasattr(request, 'intent'):
            self.intent = request.intent
            self.name = self.intent.name

        response = self.create_response()

        if hasattr(request, 'type'):
            if request.type == "LaunchRequest":
                response.object_content = self.on_launch(request, session)

            elif request.type == "IntentRequest":
                response.object_content = self.on_intent(request, session)

            elif request.type == "SessionEndedRequest":
                response.object_content = self.on_session_ended(request, session)

        """
            if request['type'] == "LaunchRequest":
                if hasattr(self, 'on_launch'):
                    response.object_content = self.on_launch(request, session)

            elif request['type'] == "IntentRequest":
                if hasattr(self, 'on_intent'):
                    response.object_content = self.on_intent(request, session)

            elif request['type'] == "SessionEndedRequest":
                if hasattr(self, 'on_session_ended'):
                    response.object_content = self.on_session_ended(request, session)
        """

        response.status_code = '200 OK'

        # debug.log('response', response)

        return response

    def on_launch(self, launch_request, session):
        # debug.logline("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])

        return self.get_welcome_response()

    def on_intent(self, request, session):
        # debug.logline("on_intent requestId=" + request['requestId'] + ", sessionId=" + session['sessionId'])

        return self.run_intent(self.name, request, session)

    def on_session_ended(self, session_ended_request, session):
        # debug.logline("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])
        pass

    def on_session_started(self, session_started_request, session):
        # debug.logline("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])
        pass

    def build_speechlet_response(self, title, output, reprompt_text, should_end_session):
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Simple',
                'title': 'SessionSpeechlet - ' + title,
                'content': 'SessionSpeechlet - ' + output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }


    def build_response(self, session_attributes, speechlet_response):
        return {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': speechlet_response
        }
