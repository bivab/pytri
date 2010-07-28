from continuation import EndContinuation, PropContinuation, KeepLookingContinuation
from pypy.rlib import jit

class Proposition(object):
    __slots__ = ()
    _immutable_ = True
    def __init__(self):
        pass

    def evaluate(self, state, *args):
        raise NameError

    @jit.purefunction
    def label(self):
        raise NameError

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __neq__(self, other):
        return not self == other

class LessProposition(Proposition):
    __slots__ = ('left', 'right')
    _immutable_ = True
    def __init__(self, left, right):
        Proposition.__init__(self)
        self.left = left
        self.right = right

    def evaluate(self, state, s, f):
        if self.left.eval(state) < self.right.eval(state):
            return s, f, state
        return f, s, state

    @jit.purefunction
    def label(self):
        return "(%s < %s)" % (self.left.label(), self.right.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.left == other.left and self.right == other.right

    __str__ = label
    __repr__ = label

class EqualsProposition(Proposition):
    _immutable_ = True
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, state, s, f):
        if self.left.eval(state) == self.right.eval(state):
            return s, f, state
        return f, s, state

    @jit.purefunction
    def label(self):
        return "(%s = %s)" % (self.left.label(), self.right.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.left == other.left and self.right == other.right

    __str__ = label
    __repr__ = label

class TrueProposition(Proposition):
    _immutable_ = True

    def evaluate(self, state, s, f):
        return s, f, state

    @jit.purefunction
    def label(self):
        return "true"

    __str__ = label
    __repr__ = label

class FalseProposition(Proposition):
    _immutable_ = True

    def evaluate(self, state, s, f):
       return f, s, state

    @jit.purefunction
    def label(self):
        return "false"

    __str__ = label
    __repr__ = label

class NegationProposition(Proposition):
    _immutable_ = True

    def __init__(self, proposition):
        self.proposition = proposition

    def evaluate(self, state, s, f):
        return PropContinuation(self.proposition, f, s), s, state

    @jit.purefunction
    def label(self):
        return "not(%s)" % self.proposition.label()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.proposition == other.proposition

    __str__ = label
    __repr__ = label

class AndProposition(Proposition):
    _immutable_ = True

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, state, s, f):
        return PropContinuation(self.left, PropContinuation(self.right, s, f), f), EndContinuation(False), state

    @jit.purefunction
    def label(self):
        return "and(%s, %s)" % (self.left.label(), self.right.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.left == other.left and self.right == other.right

    __str__ = label
    __repr__ = label


def OrProposition(left, right):
    return NegationProposition(AndProposition(NegationProposition(left), NegationProposition(right)))

class EUProposition(Proposition):
    __slots__ = ('first', 'second')
    _immutable_ = True
    def __init__(self, first, second):
        self.first = first
        self.second = second

    @jit.purefunction
    def label(self):
        return 'E(%s U %s)' % (self.first.label(), self.second.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.first == other.first and self.second == other.second

    __str__ = label
    __repr__ = label

    def evaluate(self, state, s, f):
        k = KeepLookingContinuation(self, s, f, state.successors())
        nf = PropContinuation(self.first, k, f)
        return PropContinuation(self.second, s, nf), f, state

class EGProposition(Proposition):
    __slots__ = 'proposition'
    _immutable_ = True

    def __init__(self, proposition):
        self.proposition = proposition

    @jit.purefunction
    def label(self):
        return 'EG(%s)' % (self.proposition.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.proposition == other.proposition

    __str__ = label
    __repr__ = label

    def evaluate(self, state, s, f):
        # XXX build successors lazily in another cont
        return PropContinuation(self.proposition,
                KeepLookingContinuation(self, s, f, state.successors(), True), f, True), f, state

class EXProposition(Proposition):
    __slots__ = 'proposition'
    _immutable_ = True
    def __init__(self, proposition):
        self.proposition = proposition

    @jit.purefunction
    def label(self):
        return 'EX(%s)' % (self.proposition.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.proposition == other.proposition

    __str__ = label
    __repr__ = label

    def evaluate(self, state, s, f):
        states = state.successors()
        next_state = states.pop()
        next_cont = KeepLookingContinuation(self.proposition, s, f, states)
        return PropContinuation(self.proposition, s, next_cont), f, next_state
