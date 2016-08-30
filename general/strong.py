class Strong(object):
    """
    A class to convert a nested Dictionary into an object with key-values
    accessibly using attribute notation (Strong.attribute) instead of
    key notation (Dict["key"]). This class recursively sets Dicts to objects,
    allowing you to recurse down nested dicts (like: Strong.attr.attr)
    """
    def __init__(self, **entries):
        self.add_entries(**entries)

    def add_entries(self, **entries):
        for key, value in entries.items():
            if type(value) is dict:
                self.__dict__[key] = Strong(**value)
            else:
                self.__dict__[key] = value

    def __getitem__(self, key):
        """
        Provides dict-style access to attributes
        """
        if hasattr(self, key):
            return getattr(self, key)
        else:
            return None
