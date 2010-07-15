class Animator(object):
    def __init__(self, net, state):
        self.stack = [state]
        self.net = net
        self.states = {state:state}

    def step(self):
        state = self.stack.pop()
        if state.successors is not None:
            return
        states = [self._get_state_from_cache(t.fire(state))
            for t in self.net.enabled_transitions(state)]
        self.stack.extend(states)
        state.successors = states

    def _get_state_from_cache(self, state):
        return self.states.setdefault(state, state)
