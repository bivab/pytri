from pypy.rlib import jit
class Expression(object):
    __slots__ = 'value'
    _immutable_ = True
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.value == other.value

    def label(self):
        raise NotImplementedError('abstract base class')

    def eval(self, state):
        raise NotImplementedError('abstract base class')

class NumericExpression(Expression):
    _immutable_ = True
    def __init__(self,value):
        Expression.__init__(self, value)

    @jit.purefunction
    def eval(self, state):
        return self.value

    @jit.purefunction
    def label(self):
        return "%d" % self.value

    __str__ = label
    __repr__ = label

class VariableExpression(Expression):
    _immutable_ = True
    def __init__(self,value):
        assert value >= 0
        Expression.__init__(self, value)

    @jit.purefunction
    def eval(self, state):
        return state.get(self.value)

    @jit.purefunction
    def label(self):
        return "$%d" % self.value

    __str__ = label
    __repr__ = label
