class Animator(object):
    def __init__(self, net, state):
        self.stack = [state]
        self.net = net

    def step(self):
        state = self.stack.pop()
        if state._successors is not None:
            return
        states = [self.net._get_state_from_cache(t.fire(state))
            for t in self.net.enabled_transitions(state)]
        self.stack.extend(states)
        state._successors = states

    def run(self):
        while self.stack:
            self.step()
