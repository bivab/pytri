class Proposition(object):
    def __init__(self):
        pass

    def evaluate(self, state, *args):
        raise NameError

class LessProposition(Proposition):
    def __init__(self, left, right):
        Proposition.__init__(self)
        self.left = left
        self.right = right

    def evaluate(self, state):
        return state.evaluate(self.left) < state.evaluate(self.right)

class TrueProposition(Proposition):
    def evaluate(self, state):
        return True

class FalseProposition(Proposition):
    def evaluate(self, state):
        return False

class NegationProposition(Proposition):
    def __init__(self, proposition):
        self.proposition = proposition

    def evaluate(self, state):
        return not state.evaluate(self.proposition)

    def __repr__(self):
        return "Negation: %r" % self.proposition

class AndProposition(Proposition):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, state):
        return state.evaluate(self.left) and state.evaluate(self.right)

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

def OrProposition(left, right):
    return NegationProposition(AndProposition(NegationProposition(left), NegationProposition(right)))
