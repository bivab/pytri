from propositions import LessProposition, NegationProposition, TrueProposition
from propositions import FalseProposition, AndProposition, EqualsProposition
from propositions import OrProposition

def test_less_proposition():
    assert LessProposition(1,2).evaluate(None) == True
    assert LessProposition(999999999,2).evaluate(None) == False

def test_basic_props():
    assert TrueProposition().evaluate(None) == True
    assert FalseProposition().evaluate(None) == False

def test_negation():
    assert NegationProposition(TrueProposition()).evaluate(None) == False
    assert NegationProposition(FalseProposition()).evaluate(None) == True

def test_and_proposition():
    assert AndProposition(TrueProposition(), TrueProposition()).evaluate(None) == True
    assert AndProposition(FalseProposition(), TrueProposition()).evaluate(None) == False
    assert AndProposition(FalseProposition(), FalseProposition()).evaluate(None) == False
    assert AndProposition(TrueProposition(), FalseProposition()).evaluate(None) == False

def test_equals_proposition():
    assert EqualsProposition(1, 3).evaluate(None) == False
    assert EqualsProposition(3, 3).evaluate(None) == True
    assert EqualsProposition(3, 1).evaluate(None) == False

def test_or_proposition():
    assert OrProposition(TrueProposition(), TrueProposition()).evaluate(None) == True
    assert OrProposition(FalseProposition(), TrueProposition()).evaluate(None) == True
    assert OrProposition(FalseProposition(), FalseProposition()).evaluate(None) == False
    assert OrProposition(TrueProposition(), FalseProposition()).evaluate(None) == True


