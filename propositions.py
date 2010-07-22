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
