from middleware import Middleware

from .general import debug, Strong, parse_querystring

from .formatters import active_formatters

class ResponseMiddleware(Middleware):
    def create(self):
        def func(mwa, context):
            try:
                match_found = context['match_found']
            except:
                match_found = False

            (env, response, http_accept_array) = self.read(context, 'env', 'response', 'http_accept_array')

            if not match_found:
                context['status'] = '404'
                return next(mwa)

            if response.status_code is None:
                raise HTTPError("No status code set", 400, "adsf")
            elif response.status_code == 200:
                status = "200 OK"
            else:
                status = str(response.status_code)

            context['status'] = status

            response_headers = []
            context['response_headers'] = response_headers

            result = None

            if response.string_content is not None:
                result = response.string_content

            if result is None and response.object_content is not None:
                dumps_args = {}
                http_accept = ''
                if(len([x for x in env['X-parameters'] if x[0] == 'pretty']) > 0):
                    dumps_args = {'indent': 4}

                if(len([x for x in env['X-parameters'] if x[0] == 'json']) > 0):
                    if 'application/json' not in http_accept_array:
                        http_accept_array.insert(0, 'application/json')

                formatter = None
                for http_accept in http_accept_array:
                    if http_accept in active_formatters:
                        formatter = active_formatters[http_accept]
                        break

                if formatter is None and len(active_formatters) > 0 and http_accept_array[0] == '' or http_accept_array[0] == '*/*':
                    #++ json is default for now
                    formatter_found = [v for k,v in active_formatters.items() if k == 'application/json']
                    if formatter_found is not None and len(formatter_found) > 0:
                        formatter = formatter_found[0]

                if formatter is None:
                    raise ValueError('No formatters are registered')

                result = formatter.write(response.object_content, **dumps_args)

            try:
                response.content_type = result[1]
            except:
                pass

            if response.content_type is not None:
                response_headers.append(('Content-Type', response.content_type))

            #response_headers.append(('X-Debug', "true"))

            context["result"] = result[0] if result is not None else result

            return next(mwa)

        return func
