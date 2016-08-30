class FormatterBase():
    def __init__(self):
        self.formats = []
        pass

    def get_formats(self):
        return self.formats

    def __repr__(self):
        return ', '.join(self.get_formats())