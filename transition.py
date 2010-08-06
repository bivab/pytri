from state import State

class Transition(object):
    def __init__(self, input=None, output=None):
        assert input is not None
        assert output is not None
        self.input = input
        self.output = output

    def fire(self, state):
        result = list(state.tokens)
        for place in self.input:
            result[place] -= 1
        for place in self.output:
            result[place] += 1
        return State(result, state.net) #???

    def can_fire(self, state):
        for p in self.input:
            if state.tokens[p] < 1:
                return False
        return True

    def __str__(self):
        return ''.join([str(self.input), '->', str(self.output)])
    __repr__ = __str__
