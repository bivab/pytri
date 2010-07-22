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

    def evaluate(self, state):
        return state.evaluate(self.left) < state.evaluate(self.right)

    def label(self):
        return "(%s < %s)" % (self.left.label(), self.right.label())

    __str__ = label
    __repr__ = label

class TrueProposition(Proposition):
    def evaluate(self, state):
        return True

    def label(self):
        return "true"

    __str__ = label
    __repr__ = label

class FalseProposition(Proposition):
    def evaluate(self, state):
        return False

    def label(self):
        return "false"

    __str__ = label
    __repr__ = label

class NegationProposition(Proposition):
    def __init__(self, proposition):
        self.proposition = proposition

    def evaluate(self, state):
        return not state.evaluate(self.proposition)

    def label(self):
        return "not(%s)" % self.proposition.label()

    __str__ = label
    __repr__ = label

class AndProposition(Proposition):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, state):
        return state.evaluate(self.left) and state.evaluate(self.right)

    def label(self):
        return "and(%s, %s)" % (self.left.label(), self.right.label())

    __str__ = label
    __repr__ = label

class EqualsProposition(Proposition):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, state):
        return state.evaluate(self.left) == state.evaluate(self.right)
        # cause == is too easy
        # return AndProposition(NegationProposition(
        #    LessProposition(self.left, self.right)),
        #    NegationProposition(
        #        LessProposition(self.right, self.left))).evaluate(state)

    def label(self):
        return "(%s = %s)" % (self.left.label(), self.right.label())

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

    def evaluate(self, state):
        if state.evaluate(self.second):
            return True
        if not state.evaluate(self.first):
            return False
        for s in state.successors():
            if s.evaluate(self, False):
                return True
        return False

class EGProposition(Proposition):
    def __init__(self, proposition):
        self.proposition = proposition

    def label(self):
        return 'EG(%s)' % (self.proposition.label())

    __str__ = label
    __repr__ = label

    def evaluate(self, state):
        if not state.evaluate(self.proposition):
            return False
        for s in state.successors():
            if s.evaluate(self, True):
                return True
        return False

class EXProposition(Proposition):
    def __init__(self, proposition):
        self.proposition = proposition

    def label(self):
        return 'EX(%s)' % (self.proposition.label())

    __str__ = label
    __repr__ = label

    def evaluate(self, state):
        for s in state.successors():
            if s.evaluate(self.proposition):
                return True
        return False
