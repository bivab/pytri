class Expression(object):
    def __init__(self, value):
        self.value = value

class NumericExpression(Expression):
    def __init__(self,value):
        Expression.__init__(self, value)

    def evaluate(self, state):
        return self.value

class VariableExpression(Expression):
    def __init__(self,value):
        Expression.__init__(self, value)

    def evaluate(self, state):
        return state.get(self.value)