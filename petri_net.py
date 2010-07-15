from state import State
class PetriNet(object):

    def __init__(self, transitions=None):
        if transitions is None:
            transitions = []
        self.transitions = transitions
        self.places = self.get_places()

    def enabled_transitions(self):
        return [c for c in self.transitions if c.can_fire()]

    def state(self):
        return State([t.tokens for t in self.places])

    def get_places(self):
        t = {}
        for transition in self.transitions:
            for p in transition.input:
                t[p] = None
            for p in transition.output:
                t[p] = None
        return t.keys()
