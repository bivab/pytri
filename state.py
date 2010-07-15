class State(object):
    def __init__(self, tokens=None):
        if tokens is None:
            tokens = []
        self.tokens = tokens

    def __eq__(self, other):
        return self.tokens == other.tokens

    def __ne__(self, other):
        return not self == other
