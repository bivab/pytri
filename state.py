from continuation import PropContinuation, EndContinuation, Continuation
from pypy.rlib import jit
from pypy.rlib.objectmodel import specialize
from pypy.rlib import rarithmetic

def get_printable_location(prop):
    if prop:
        l = str(prop) + str(prop.label())
    else:
        l = 'No Prop'
    return l

jitdriver = jit.JitDriver(
                reds=["cont", "f", "state"],
                greens=["prop"],
                get_printable_location=get_printable_location,
            )

def state_eq(self, other):
        assert isinstance(other, type(self))
        for x in range(len(self.tokens)):
            if self.tokens[x] != other.tokens[x]:
                return False
        return True

def state_hash(state):
    return state.hash()

class State(object):
    _immutable_ = True
    __slots__ = ('tokens', 'net','labels', '_hash')
    def __init__(self, tokens=None, net=None):
        if tokens is None:
            tokens = []
        self.tokens = tokens
        self.net = net
        self._hash = 0
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

    @jit.purefunction
    def hash(self):
        if self._hash:
            return self._hash
        x = 0x345678
        for i in range(len(self.tokens)):
            y = self.tokens[i]
            x = rarithmetic.intmask((1000003 * x) ^ y)
        self._hash = x
        return x

    equals = state_eq
    __eq__ = equals
    __hash__ = hash

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'State(%r)' % self.tokens
