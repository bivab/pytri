from continuation import PropContinuation, EndContinuation, Continuation
from pypy.rlib import jit
from pypy.rlib.objectmodel import specialize
jitdriver = jit.JitDriver(reds=["cont", "f", "state"], greens=["prop"])

class State(object):
    def __init__(self, tokens=None, net=None):
        if tokens is None:
            tokens = []
        self.tokens = tokens
        self.net = net
        self._successors = None
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

    @specialize.argtype(0)
    def equals(self, other):
        return self.tokens == other.tokens

    __eq__ = equals

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self.tokens))

    def __repr__(self):
        return 'State(%r)' % self.tokens
