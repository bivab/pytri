class State(object):
    def __init__(self, tokens=None):
        if tokens is None:
            tokens = []
        self.tokens = tokens
        self.successors = None
        self.labels = {}
    def get(self, i):
        return self.tokens[i]

    def evaluate(self, prop):
        if prop in self.labels:
            return self.labels[prop]
        self.labels[prop] = prop.evaluate(self)
        return self.labels[prop]

    def __eq__(self, other):
        return self.tokens == other.tokens

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self.tokens))

    def __repr__(self):
        return 'State(%r)' % self.tokens
