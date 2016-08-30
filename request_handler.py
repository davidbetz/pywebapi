import json

from .general import debug

from .resource_base import ResourceBase

from .response import Response

class RequestHandler(ResourceBase):
    def __init__(self, repo):
        # debug.logline('item:__init__ called')
        self.repo = repo

    def post(self, env, obj, *args):
        # debug.logline('item:post called')
        # debug.log('obj', obj)
        # debug.log('args', args)

        response = self.create_response()

        '''
        obj = self.get_body_object(body)
        if obj is None:
            response.string_content = "invalid"
            response.status_code = 400
            return response
        '''

        id = self.get_arg(args, 0)
        if id is None:
            response = self.create_response()

            try:
                response.string_content = str(self.repo.set(obj))
                response.status_code = 200
            except:
                raise
                response.status_code = 500

            return response

        existing_obj = self.repo.get(id)
        if existing_obj is None:
            response.string_content = "not found"
            response.status_code = 404
            return response

        try:
            self.repo.set_param(id, obj, existing_obj = existing_obj)
            response.status_code = 204
        except:
            raise
            response.status_code = 500

        return response

    def put(self, env, obj, *args):
        # debug.logline('item:put called')
        # debug.log('obj', obj)
        # debug.log('args', args)

        response = self.create_response()

        '''
        obj = self.get_body_object(body)
        if obj is None:
            response.string_content = "invalid data"
            response.status_code = 500
            return response
        '''

        id = self.get_arg(args, 0)
        if id is None:
            response.string_content = "PUT requires an id"
            response.status_code = 501
            return response

        existing_obj = self.repo.get(id)
        if existing_obj is None:
            try:
                response.string_content = str(self.repo.set(obj))
                response.status_code = 200
            except:
                raise
        else:
            try:
                self.repo.set_param(id, obj, existing_obj = existing_obj)
                response.status_code = 204
            except:
                response.status_code = 500

        return response

    def get(self, env, *args):
        # debug.logline('item:get')

        # debug.log('args', args)

        id = self.get_arg(args, 0)
        response = self.create_response()

        if id is None:
            response.object_content = self.repo.all()
            response.status_code = 200
            return response

        # debug.log('id', id)

        item = self.repo.get(id)

        # debug.log('self.repo.items', self.repo.items)

        if item is not None:
            response.object_content = item
            response.status_code = 200
        else:
            response.status_code = 404

        return response

    def delete(self, env, *args):
        response = self.create_response()

        id = self.get_arg(args, 0)
        debug.logline('RequestHandler::delete|id' + id)
        if id is None:
            response.string_content = "DELETE requires an id"
            response.status_code = 500
            return response

        '''
        #++ does this even matter?
        existing_obj = self.repo.get(id)
        if existing_obj is None:
            pass
            #response.string_content = "not found"
            #response.status_code = 404
            #return response
        '''

        try:
            self.repo.remove(id)
            response.status_code = 204
        except:
            raise
            response.status_code = 500
            response.string_content = "error deleting"

        return response