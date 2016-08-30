class Processor():
    def __init__(self):
        pass

    def home(self, **context):
        return 'home page'

    def contact(self, **context):
        return {
            "hello": 2
        }

    def contact_post(self, **context):
        return {
            "this was": "a post"
        }