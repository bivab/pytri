class State(object):
    def __init__(self, tokens=None, net=None):
        if tokens is None:
            tokens = []
        self.tokens = tokens
        self.net = net
        self._successors = None
        self.labels = {}

    def successors(self):
        return [self.net._get_state_from_cache(t.fire(self)) for t in self.net.enabled_transitions(self)]

    def get(self, i):
        return self.tokens[i]

    def evaluate(self, prop, default = False):
        if prop in self.labels:
            return self.labels[prop]
        self.labels[prop] = default
        self.labels[prop] = prop.evaluate(self)
        return self.labels[prop]

    def __eq__(self, other):
        return self.tokens == other.tokens

    equals = __eq__

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self.tokens))

    def __repr__(self):
        return 'State(%r)' % self.tokens
