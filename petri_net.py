from state import State
class PetriNet(object):

    def __init__(self, transitions=None):
        if transitions is None:
            transitions = []
        self.transitions = transitions

    def enabled_transitions(self, state):
        return [c for c in self.transitions if c.can_fire(state)]

