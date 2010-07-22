from animator import Animator
from propositions import FalseProposition, AndProposition, EqualsProposition
from propositions import LessProposition, NegationProposition, TrueProposition
from propositions import OrProposition, EUProposition, EGProposition
from state import State
from petri_net import PetriNet
from transition import Transition
from expression import VariableExpression, NumericExpression

state = State([2,0,0,1,0])
def test_less_than():
    assert state.evaluate(LessProposition(VariableExpression(3), VariableExpression(0))) == True
    assert state.evaluate(LessProposition(VariableExpression(0), VariableExpression(3))) == False

    assert state.evaluate(LessProposition(NumericExpression(123412), VariableExpression(3))) == False
    assert state.evaluate(LessProposition(NumericExpression(-1), VariableExpression(3))) == True

def test_less_proposition():
    assert state.evaluate(LessProposition(NumericExpression(1),NumericExpression(2))) == True
    assert state.evaluate(LessProposition(NumericExpression(999999999),NumericExpression(2))) == False

def test_basic_props():
    assert state.evaluate(TrueProposition()) == True
    assert state.evaluate(FalseProposition()) == False

def test_negation():
    assert state.evaluate(NegationProposition(TrueProposition())) == False
    assert state.evaluate(NegationProposition(FalseProposition())) == True

def test_and_proposition():
    assert state.evaluate(AndProposition(TrueProposition(), TrueProposition())) == True
    assert state.evaluate(AndProposition(FalseProposition(), TrueProposition())) == False
    assert state.evaluate(AndProposition(FalseProposition(), FalseProposition())) == False
    assert state.evaluate(AndProposition(TrueProposition(), FalseProposition())) == False

def test_equals_proposition():
    assert state.evaluate(EqualsProposition(NumericExpression(1), NumericExpression(3))) == False
    assert state.evaluate(EqualsProposition(NumericExpression(3), NumericExpression(3))) == True
    assert state.evaluate(EqualsProposition(NumericExpression(3), NumericExpression(1))) == False

def test_or_proposition():
    assert state.evaluate(OrProposition(TrueProposition(), TrueProposition())) == True
    assert state.evaluate(OrProposition(FalseProposition(), TrueProposition())) == True
    assert state.evaluate(OrProposition(FalseProposition(), FalseProposition())) == False
    assert state.evaluate(OrProposition(TrueProposition(), FalseProposition())) == True


def test_petri_net_with_propositions():
    t = Transition([0], [1])
    p = PetriNet([t])
    s1 = State([1,0], p)
    assert s1.evaluate(AndProposition(EqualsProposition(VariableExpression(0), NumericExpression(1)),
                                    EqualsProposition(VariableExpression(1), NumericExpression(0))))
    a = Animator(p, s1)
    a.step()
    s2 = s1.successors()[0]
    assert s2.evaluate(AndProposition(EqualsProposition(VariableExpression(0), NumericExpression(0)),
                                    EqualsProposition(VariableExpression(1),
                                    NumericExpression(1))))


def test_eu_proposition():
    t = Transition([0], [1])
    p = PetriNet([t])
    s1 = State([5,0], p)
    prop = EUProposition(LessProposition(NumericExpression(0),
    VariableExpression(0)), EqualsProposition(VariableExpression(1), NumericExpression(3)))
    assert s1.evaluate(prop) == True

def test_eu_proposition_1():
    t = Transition([0], [1])
    p = PetriNet([t])
    s1 = State([0,2], p)
    prop = EUProposition(LessProposition(NumericExpression(0),
    VariableExpression(0)), EqualsProposition(VariableExpression(1), NumericExpression(3)))
    assert s1.evaluate(prop) == False

def test_eu_proposition_2():
    t = Transition([0], [1])
    p = PetriNet([t])
    s1 = State([0,2], p)
    prop = EUProposition(LessProposition(NumericExpression(0),
    VariableExpression(0)), TrueProposition())
    assert s1.evaluate(prop) == True

def test_eu_loop():
    t = Transition([0], [0])
    p = PetriNet([t])
    state = State([1], p)
    prop = EUProposition(TrueProposition(), FalseProposition())
    state.evaluate(prop) # should terminate
    assert len(p._states_cache) == 1

def test_eg_loop():
    t = Transition([0], [0])
    p = PetriNet([t])
    state = State([1], p)
    prop = EGProposition(TrueProposition())
    assert state.evaluate(prop) == True
    assert len(p._states_cache) == 1

def test_eg_five():
    t = Transition([0], [1])
    p = PetriNet([t])
    s1 = State([5,0], p)
    prop = EGProposition(LessProposition(NumericExpression(0), VariableExpression(0)))
    assert s1.evaluate(prop) == False

def test_dual_loop():
    t1 = Transition([0], [1])
    t2 = Transition([1], [0])
    p = PetriNet([t1, t2])
    state = State([0, 1], p)
    prop = EGProposition(TrueProposition())
    assert state.evaluate(prop) == True


