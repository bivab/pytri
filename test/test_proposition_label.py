from animator import Animator
from propositions import FalseProposition, AndProposition, EqualsProposition
from propositions import LessProposition, NegationProposition, TrueProposition
from propositions import OrProposition, EUProposition
from expression import VariableExpression, NumericExpression

def test_labels():
    assert LessProposition(VariableExpression(3), VariableExpression(0)).label() == "($3 < $0)"
    assert LessProposition(VariableExpression(0), VariableExpression(3)).label() == '($0 < $3)'
    assert LessProposition(NumericExpression(123412), VariableExpression(3)).label() == '(123412 < $3)'
    assert LessProposition(NumericExpression(-1), VariableExpression(3)).label() == '(-1 < $3)'
    assert AndProposition(EqualsProposition(VariableExpression(0), NumericExpression(1)),
                                    EqualsProposition(VariableExpression(1),
                                    NumericExpression(0))).label() == 'and(($0 = 1), ($1 = 0))'

def test_eu_label():
    assert EUProposition(TrueProposition(), FalseProposition()).label() == 'E(true U false)'
