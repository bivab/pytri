from state import State
class PetriNet(object):

    def __init__(self, transitions=None):
        if transitions is None:
            transitions = []
        self.transitions = transitions
        self._states_cache = {}

    def _get_state_from_cache(self, state):
        return self._states_cache.setdefault(state.hash(), state)

    def enabled_transitions(self, state):
        return [c for c in self.transitions if c.can_fire(state)]

