from continuation import PropContinuation, EndContinuation, Continuation
from pypy.rlib import jit
from pypy.rlib.objectmodel import specialize
jitdriver = jit.JitDriver(reds=["cont", "f", "state"], greens=["prop"])

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

    def equals(self, other):
        assert isinstance(other, type(self))
        for x in range(len(self.tokens)):
            if self.tokens[x] != other.tokens[x]:
                return False
        return True

    __eq__ = equals

    def __ne__(self, other):
        return not self == other


    def hash(self):
        result = 0
        # XXX correct?
        for i in range(len(self.tokens)):
            result += (1+i) * 17 * self.tokens[i]
        return result

    __hash__ = hash

    def __repr__(self):
        return 'State(%r)' % self.tokens
