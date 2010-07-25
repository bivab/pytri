class Continuation(object):
    def __init__(self):
        pass

    def is_done(self):
        return False

class PropContinuation(Continuation):
    def __init__(self, prop, succ, fail, mark = False):
        self.prop = prop
        self.succ = succ
        self.fail = fail
        self.mark = mark

    def activate(self, state):
        label = self.prop.label()
        if label in state.labels:
            if state.labels[label]:
                return self.succ, self.fail, state
            else:
                return self.fail, self.succ, state
        state.labels[label] = self.mark
        m1 = MarkContinuation(self.prop, state, self.succ, self.succ, True)
        m2 = MarkContinuation(self.prop, state, self.fail, self.fail, False)
        return self.prop.evaluate(state, m1, m2)

class KeepLookingContinuation(PropContinuation):
    def __init__(self, prop, s, f, states, mark=False):
        PropContinuation.__init__(self, prop, s, f)
        self.states = states
        self.i = len(states)
        self.mark = mark

    def activate(self, state):
        self.i -= 1
        if self.i > 0:
            return PropContinuation(self.prop, self.succ, self, self.mark), self.fail, self.states[self.i]
        if self.i == 0:
            return PropContinuation(self.prop, self.succ, self.fail, self.mark), self.fail, self.states[0]
        # XXX why?
        if self.i < 0:
            return self.succ, self.fail, state

class MarkContinuation(PropContinuation):
    def __init__(self, prop, state, succ, fail, mark=False):
        PropContinuation.__init__(self, prop, succ, fail)
        self.state = state
        self.mark = mark

    def activate(self, state):
        self.state.labels[self.prop.label()] = self.mark
        return self.succ, self.fail, state

class EndContinuation(Continuation):
    def __init__(self, result):
        Continuation.__init__(self)
        self.result = result

    def is_done(self):
        return True
