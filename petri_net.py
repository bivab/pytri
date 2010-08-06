from state import State, state_hash, state_eq
from pypy.rlib.objectmodel import r_dict
class PetriNet(object):

    def __init__(self, transitions=None):
        if transitions is None:
            transitions = []
        self.transitions = transitions
        self._states_cache = r_dict(state_eq, state_hash)

    def _get_state_from_cache(self, state):
        return self._states_cache.setdefault(state, state)

    def enabled_transitions(self, state):
        return [c for c in self.transitions if c.can_fire(state)]

    def __str__(self):
        result = []
        for t in self.transitions:
            result.append(str(t))
            result.append('\n')
        return ''.join(result)


