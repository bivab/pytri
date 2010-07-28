from expression import NumericExpression, VariableExpression
from state import State

def test_numeric_expression():
    n = NumericExpression(4)
    assert n.eval(None) == 4

def test_variable_expression():
    v = VariableExpression(1)
    assert v.eval(State([123123, 3])) == 3
