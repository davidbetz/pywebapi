class Response():
    def __init__(self):
        self.string_content = None
        self.object_content = None
        self.content_type = None
        self.status_code = 0

    def __repr__(self):
        content = ''
        if self.string_content is not None:
            content += 'string_content: {}'.format(self.string_content)

        if self.object_content is not None:
            content += 'object_content: {}'.format(self.object_content)

        if self.content_type is not None:
            content += 'content_type: {}'.format(self.content_type)

        if self.status_code is not None:
            content += 'status_code: {}'.format(self.status_code)

        return content