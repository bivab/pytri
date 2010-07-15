class Place(object):
    def __init__(self, tokens = 0):
        if tokens < 0:
            raise ValueError('tokens must be >= 0')
        self.tokens = tokens

