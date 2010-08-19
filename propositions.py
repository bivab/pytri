from continuation import EndContinuation, PropContinuation
from continuation import EXContinuation, EUContinuation, EGContinuation
from pypy.rlib import jit

class Proposition(object):
    __slots__ = ('cached_label', )
    _immutable_ = True
    def __init__(self):
        self.cached_label = None

    def evaluate(self, state, *args):
        raise NotImplementedError('abstract base class')

    def _label(self):
        raise NotImplementedError('abstract base class')

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __neq__(self, other):
        return not self == other

    @jit.purefunction
    def label(self):
        if not self.cached_label:
            self.cached_label = self._label()
        return self.cached_label

    __str__ = label
    __repr__ = label

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
    def _label(self):
        return "(%s < %s)" % (self.left.label(), self.right.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.left == other.left and self.right == other.right


class EqualsProposition(Proposition):
    _immutable_ = True
    def __init__(self, left, right):
        Proposition.__init__(self)
        self.left = left
        self.right = right

    def evaluate(self, state, s, f):
        if self.left.eval(state) == self.right.eval(state):
            return s, f, state
        return f, s, state

    @jit.purefunction
    def _label(self):
        return "(%s = %s)" % (self.left.label(), self.right.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.left == other.left and self.right == other.right


class TrueProposition(Proposition):
    _immutable_ = True

    def evaluate(self, state, s, f):
        return s, f, state

    @jit.purefunction
    def _label(self):
        return "true"


class FalseProposition(Proposition):
    _immutable_ = True

    def evaluate(self, state, s, f):
       return f, s, state

    @jit.purefunction
    def _label(self):
        return "false"


class NegationProposition(Proposition):
    _immutable_ = True

    def __init__(self, proposition):
        Proposition.__init__(self)
        self.proposition = proposition

    def evaluate(self, state, s, f):
        return PropContinuation(self.proposition, f, s), s, state

    @jit.purefunction
    def _label(self):
        return "not(%s)" % self.proposition.label()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.proposition == other.proposition


class AndProposition(Proposition):
    _immutable_ = True

    def __init__(self, left, right):
        Proposition.__init__(self)
        self.left = left
        self.right = right

    def evaluate(self, state, s, f):
        return PropContinuation(self.left, PropContinuation(self.right, s, f), f), EndContinuation(False), state

    @jit.purefunction
    def _label(self):
        return "and(%s, %s)" % (self.left.label(), self.right.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.left == other.left and self.right == other.right



def OrProposition(left, right):
    return NegationProposition(AndProposition(NegationProposition(left), NegationProposition(right)))

class EUProposition(Proposition):
    __slots__ = ('first', 'second')
    _immutable_ = True
    def __init__(self, first, second):
        Proposition.__init__(self)
        self.first = first
        self.second = second

    @jit.purefunction
    def _label(self):
        return 'E(%s U %s)' % (self.first.label(), self.second.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.first == other.first and self.second == other.second


    def evaluate(self, state, s, f):
        ff = EUContinuation(self, s, f)
        fail = PropContinuation(self.first, ff, f)
        return PropContinuation(self.second, s, fail), f, state

class EGProposition(Proposition):
    __slots__ = 'proposition'
    _immutable_ = True

    def __init__(self, proposition):
        Proposition.__init__(self)
        self.proposition = proposition

    @jit.purefunction
    def _label(self):
        return 'EG(%s)' % (self.proposition.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.proposition == other.proposition


    def evaluate(self, state, s, f):
        p = EGContinuation(self, s, f)
        return PropContinuation(self.proposition, p, f, False), f, state

class EXProposition(Proposition):
    __slots__ = 'proposition'
    _immutable_ = True
    def __init__(self, proposition):
        Proposition.__init__(self)
        self.proposition = proposition

    @jit.purefunction
    def _label(self):
        return 'EX(%s)' % (self.proposition.label())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.proposition == other.proposition


    def evaluate(self, state, s, f):
        return EXContinuation(self.proposition, state, s, f), f, state
