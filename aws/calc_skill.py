from ..general.debug import kwlog, log, logline, logargs

from .skill_base import SkillBase

class CalcSkill(SkillBase):
    def __init__(self):
        self.application_id = 'amzn1.echo-sdk-ams.app.b0e6439a-f5b1-4a47-89fc-12aa0393a265'

        self.register_intents([
            (r'AddIntent', self.add_value),
            (r'SubtractIntent', self.subtract_value),
            (r'GetValueIntent', self.get_total),
            (r'AMAZON.HelpIntent', self.get_welcome_response),
            (r'AMAZON.CancelIntent', self.handle_session_end_request),
            (r'AMAZON.StopIntent', self.handle_session_end_request),
        ])

    def get_welcome_response(self):
        session_attributes = {}
        card_title = "Welcome"
        speech_output = "Calculator started"

        reprompt_text = "Is there a value you would like to add or subtract?"
        should_end_session = False
        return self.build_response(session_attributes, self.build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


    def handle_session_end_request(self):
        card_title = "Session Ended"
        speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                        "Have a nice day! "
        # Setting this to true ends the session and exits the skill.
        should_end_session = True
        return self.build_response({}, self.build_speechlet_response(card_title, speech_output, None, should_end_session))


    def add_value(self, request, session):
        session_attributes = {}
        should_end_session = False

        value = int(self.slot_value(request, 'numericvalue')) or 0
        total = int(self.session_value(session, 'numericvalue') or 0) + value

        speech_output = "I've added {}. Total is {}".format(value, total)
        session_attributes['numericvalue'] = total
        reprompt_text = ''

        return self.build_response(session_attributes, self.build_speechlet_response(self.name, speech_output, reprompt_text, should_end_session))

    def subtract_value(self, request, session):
        session_attributes = {}
        should_end_session = False

        value = int(self.slot_value(request, 'numericvalue')) or 0
        total = int(self.session_value(session, 'numericvalue') or 0) - value

        speech_output = "I've substracted {}. Total is {}".format(value, total)
        session_attributes['numericvalue'] = total
        reprompt_text = ''

        return self.build_response(session_attributes, self.build_speechlet_response(self.name, speech_output, reprompt_text, should_end_session))

    def get_total(self, request, session):
        reprompt_text = None

        should_end_session = False

        value = self.session_value(session, 'numericvalue')
        speech_output = "The total is {}".format(value) if value != None else 'Value not yet set.'

        session_attributes = { 'numericvalue': value }

        return self.build_response(session_attributes, self.build_speechlet_response(self.name, speech_output, reprompt_text, should_end_session))

