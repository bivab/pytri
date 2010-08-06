from pypy.rlib.objectmodel import specialize
class Continuation(object):
    __slots__ = ('prop', 'mark')
    _immutable_ = True
    def __init__(self):
        pass

    def is_done(self):
        return False

    def activate(*args):
        raise NameError

class PropContinuation(Continuation):
    __slots__ = ('prop', 'succ', 'fail')
    _immutable_ = True

    def __init__(self, prop, succ, fail, mark=False):
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
    _immutable_fields_ = ["states"]
    __slots__ = ('states', 'i')

    @specialize.arg(5)
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
        if self.mark:
            return self.succ, self.fail, state
        return self.fail, self.succ, state

class EGContinuation(PropContinuation):
    _immutable_fields_ = ["states", 'state']
    __slots__ = ('states', 'state', 'i', 'activated')
    def __init__(self, prop, s, f, state):
        PropContinuation.__init__(self, prop, s, f)
        self.activated = False
        self.state = state
        self.states = state.successors()
        self.i = len(self.states)

    def activate(self, state):
        if self.activated:
            self.i -= 1
            if self.i < 0:
                return self.succ, self.fail, state
            return PropContinuation(self.prop, self, self.fail, True), self.fail, self.states[self.i]
        else:
            self.activated = True
            return PropContinuation(self.prop.proposition, self, self.fail, True), self.fail, state

class EXContinuation(PropContinuation):
    _immutable_fields_ = ["states"]
    __slots__ = ('states', 'i')

    def __init__(self, prop, state, s, f):
        PropContinuation.__init__(self, prop, s, f)
        self.states = state.successors()
        self.i = len(self.states)

    def activate(self, state):
        self.i -= 1
        if self.i >= 0:
            return PropContinuation(self.prop, self.succ, self), self.fail, self.states[self.i]
        else:
            return self.fail, self.succ, state

class MarkContinuation(PropContinuation):
    _immutable_ = True
    __slots__ = ('state')
    @specialize.arg(5)
    def __init__(self, prop, state, succ, fail, mark=False):
        PropContinuation.__init__(self, prop, succ, fail)
        self.state = state
        self.mark = mark

    def activate(self, state):
        self.state.labels[self.prop.label()] = self.mark
        return self.succ, self.fail, state

class EndContinuation(Continuation):
    _immutable_ = True
    __slots__ = ('result')

    @specialize.arg(1)
    def __init__(self, result):
        Continuation.__init__(self)
        self.result = result

    def is_done(self):
        return True
