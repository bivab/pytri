from continuation import PropContinuation, EndContinuation, Continuation
from pypy.rlib import jit
from pypy.rlib.objectmodel import specialize
jitdriver = jit.JitDriver(reds=["cont", "f", "state"], greens=["prop"])

def state_eq(self, other):
        assert isinstance(other, type(self))
        for x in range(len(self.tokens)):
            if self.tokens[x] != other.tokens[x]:
                return False
        return True

def state_hash(state):
    result = 0
    for i in range(len(state.tokens)):
        result += (i+1) * (31*(i*2)) * state.tokens[i]
    return result

class State(object):
    _immutable_ = True
    __slots__ = ('tokens', 'net','labels')
    def __init__(self, tokens=None, net=None):
        if tokens is None:
            tokens = []
        self.tokens = tokens
        self.net = net
        self.labels = {}

    def successors(self):
        return [self.net._get_state_from_cache(t.fire(self)) for t in self.net.enabled_transitions(self)]

    def get(self, i):
        return self.tokens[i]

    def evaluate(self, prop, default = False):
        f = EndContinuation(False)
        cont = PropContinuation(prop, EndContinuation(True), f)
        state = self
        while not cont.is_done():
            prop = cont.prop
            jitdriver.can_enter_jit(cont=cont, f=f, state=state, prop=prop)
            jitdriver.jit_merge_point(cont=cont, f=f, state=state, prop=prop)
            cont, f, state = cont.activate(state)
        assert isinstance(cont, EndContinuation)
        return cont.result

    equals = state_eq
    __eq__ = equals
    __hash__ = state_hash

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'State(%r)' % self.tokens
