from continuation import EndContinuation, PropContinuation, KeepLookingContinuation

class Proposition(object):
    def __init__(self):
        pass

    def evaluate(self, state, *args):
        raise NameError

    def label(self):
        raise NameError

class LessProposition(Proposition):
    def __init__(self, left, right):
        Proposition.__init__(self)
        self.left = left
        self.right = right

    def evaluate(self, state, s, f):
        if self.left.evaluate(state) < self.right.evaluate(state):
            return s, f, state
        return f, s, state

    def label(self):
        return "(%s < %s)" % (self.left.label(), self.right.label())

    __str__ = label
    __repr__ = label

class EqualsProposition(Proposition):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, state, s, f):
        if self.left.evaluate(state) == self.right.evaluate(state):
            return s, f, state
        return f, s, state

    def label(self):
        return "(%s = %s)" % (self.left.label(), self.right.label())

    __str__ = label
    __repr__ = label

class TrueProposition(Proposition):
    def evaluate(self, state, s, f):
        return s, f, state

    def label(self):
        return "true"

    __str__ = label
    __repr__ = label

class FalseProposition(Proposition):
    def evaluate(self, state, s, f):
       return f, s, state

    def label(self):
        return "false"

    __str__ = label
    __repr__ = label

class NegationProposition(Proposition):
    def __init__(self, proposition):
        self.proposition = proposition

    def evaluate(self, state, s, f):
        return PropContinuation(self.proposition, f, s), s, state

    def label(self):
        return "not(%s)" % self.proposition.label()

    __str__ = label
    __repr__ = label

class AndProposition(Proposition):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, state, s, f):
        return PropContinuation(self.left, PropContinuation(self.right, s, f), f), EndContinuation(False), state

    def label(self):
        return "and(%s, %s)" % (self.left.label(), self.right.label())

    __str__ = label
    __repr__ = label


def OrProposition(left, right):
    return NegationProposition(AndProposition(NegationProposition(left), NegationProposition(right)))

class EUProposition(Proposition):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def label(self):
        return 'E(%s U %s)' % (self.first.label(), self.second.label())

    __str__ = label
    __repr__ = label

    def evaluate(self, state, s, f):
        k = KeepLookingContinuation(self, s, f, state.successors())
        nf = PropContinuation(self.first, k, f)
        return PropContinuation(self.second, s, nf), f, state

class EGProposition(Proposition):
    def __init__(self, proposition):
        self.proposition = proposition

    def label(self):
        return 'EG(%s)' % (self.proposition.label())

    __str__ = label
    __repr__ = label

    def evaluate(self, state, s, f):
        # XXX build successors lazily in another cont
        return PropContinuation(self.proposition,
                KeepLookingContinuation(self, s, f, state.successors(), True), f, True), f, state

class EXProposition(Proposition):
    def __init__(self, proposition):
        self.proposition = proposition

    def label(self):
        return 'EX(%s)' % (self.proposition.label())

    __str__ = label
    __repr__ = label

    def evaluate(self, state, s, f):
        states = state.successors()
        next_state = states.pop()
        next_cont = KeepLookingContinuation(self.proposition, s, f, states)
        return PropContinuation(self.proposition, s, next_cont), f, next_state
