from propositions import Proposition
class Expression(Proposition):
    def __init__(self, value):
        self.value = value

class NumericExpression(Expression):
    def __init__(self,value):
        Expression.__init__(self, value)

    def evaluate(self, state):
        return self.value

    def label(self):
        return "%d" % self.value

    __str__ = label
    __repr__ = label

class VariableExpression(Expression):
    def __init__(self,value):
        assert value >= 0
        Expression.__init__(self, value)

    def evaluate(self, state):
        return state.get(self.value)

    def label(self):
        return "$%d" % self.value

    __str__ = label
    __repr__ = label
