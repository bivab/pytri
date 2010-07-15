class Transition(object):
    def __init__(self, input=None, output=None):
        assert input is not None
        assert output is not None
        self.input = input
        self.output = output

    def fire(self):
        for place in self.input:
            place.tokens -= 1
        for place in self.output:
            place.tokens += 1

    def can_fire(self):
        for p in self.input:
            if p.tokens < 1:
                return False
        return True

