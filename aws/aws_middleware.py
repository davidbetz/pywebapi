import re
import json

from middleware import Middleware

from ..general import Strong
from ..log import LogFactory
from ..resources import aws_skills

class AwsMiddleware(Middleware):
    def create(self):
        def func(mwa, context):
            match_found = context['match_found']

            if match_found:
                return next(mwa)

            (env, path, body, response, env_metadata, log_raw_messages) = self.read(context, 'env', 'path', 'body', 'response', 'env_metadata', 'log_raw_messages')

            aws_obj = json.loads(body)
            for pattern, skill in aws_skills:
                if not match_found:
                    match = re.search(pattern, path)
                    if match is not None:
                        match_found = True
                        input_args = [x for x in match.groups() if x is not None]
                        callback = skill()

                        if 'session' in aws_obj and 'request' in aws_obj:
                            raw_logger = LogFactory.create(settings.log_raw_provider) if log_raw_messages else LogFactory.create('dummy')
                            raw_logger.save(re.sub('[^0-9a-zA-Z]+', '_', pattern), { 'env': env_metadata, 'obj': aws_obj })

                            session = Strong(**aws_obj['session'])
                            request = Strong(**aws_obj['request'])

                            # debug.log('aws_obj', aws_obj)
                            # debug.log('session', session)
                            # debug.log('request', request)

                            signature = env['HTTP_SIGNATURE']
                            signature_cert_chain_url = env['HTTP_SIGNATURECERTCHAINURL'].lower()

                            # TODO: validate cert

                            if session.application.applicationId == callback.get_application_id():
                                response = callback.execute(request, session)
                            else:
                                response = callback.create_response(400, 'Invalid application id')

            self.write(context, **{ 'response': response, 'match_found': match_found})

            return next(mwa)

        return func

