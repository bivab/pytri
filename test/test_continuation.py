import py
from propositions import FalseProposition, AndProposition, EqualsProposition
from propositions import LessProposition, NegationProposition, TrueProposition
from propositions import OrProposition, EUProposition, EGProposition, EXProposition
from state import State
from petri_net import PetriNet
from transition import Transition
from expression import VariableExpression, NumericExpression
from continuation import PropContinuation, EndContinuation
from parse import parse_net, parse_props
state = State([2,0,0,1,0])

def test_prop_continuation_true_prop():
    p = PropContinuation(TrueProposition(), EndContinuation(True), EndContinuation(False))
    assert run(p, state) == True

def test_prop_continuation_false_prop():
    p = PropContinuation(FalseProposition(), EndContinuation(True), EndContinuation(False))
    i = run(p, state)
    assert i == False

def test_run_true():
    p = PropContinuation(TrueProposition(), EndContinuation(True), EndContinuation(False))
    assert run(p, state) == True

def test_run_false():
    p = PropContinuation(FalseProposition(), EndContinuation(True), EndContinuation(False))
    assert run(p, state) == False

def test_prop_and_continuation():
    p = PropContinuation(AndProposition(TrueProposition(), FalseProposition()), EndContinuation(True), EndContinuation(False))
    s, f, c = p.activate(state)
    assert s.is_done() == False
    assert s.prop.label() == 'true'
    assert s.succ.prop.label() == 'false'
    assert f.is_done() == True
    assert c is state

def test_run_and_prop():
    p = PropContinuation(AndProposition(TrueProposition(), FalseProposition()), EndContinuation(True), EndContinuation(False))
    p2 = PropContinuation(AndProposition(TrueProposition(), TrueProposition()), EndContinuation(True), EndContinuation(False))
    assert run(p, state) == False
    assert run(p2, state) == True

def test_prop_not_continuation():
    prop = NegationProposition(AndProposition(TrueProposition(), TrueProposition()))
    prop2 = NegationProposition(AndProposition(TrueProposition(), FalseProposition()))
    prop3 = NegationProposition(AndProposition(FalseProposition(), FalseProposition()))
    p = PropContinuation(prop, EndContinuation(True), EndContinuation(False))
    p2 = PropContinuation(prop2, EndContinuation(True), EndContinuation(False))
    p3 = PropContinuation(prop3, EndContinuation(True), EndContinuation(False))
    assert run(p, state) == False
    assert run(p2, state) == True
    assert run(p3, state) == True

def test_or_proposition():
    prop = OrProposition(TrueProposition(), FalseProposition())
    prop2 = OrProposition(FalseProposition(), TrueProposition())
    prop3 = OrProposition(FalseProposition(), FalseProposition())
    p = PropContinuation(prop, EndContinuation(True), EndContinuation(False))
    p2 = PropContinuation(prop2, EndContinuation(True), EndContinuation(False))
    p3 = PropContinuation(prop3, EndContinuation(True), EndContinuation(False))
    assert run(p, state) == True
    assert run(p2, state) == True
    assert run(p3, state) == False

def test_ex_proposition():
    t1 = Transition([0], [1])
    t2 = Transition([1], [2])
    p = PetriNet([t1, t2])
    s1 = State([1,1,0], p)
    prop = EXProposition(EqualsProposition(VariableExpression(0), NumericExpression(0)))
    p = PropContinuation(prop, EndContinuation(True), EndContinuation(False))
    assert run(p, s1) == True

def test_eg_proposition():
    t = Transition([0], [1])
    p = PetriNet([t])
    s1 = State([5,0], p)
    prop = EGProposition(OrProposition(LessProposition(NumericExpression(0),
    VariableExpression(0)), EqualsProposition(NumericExpression(0),
    VariableExpression(0))))
    p = PropContinuation(prop, EndContinuation(True), EndContinuation(False))
    assert run(p, s1) == True

def test_eu_proposition_1():
    t = Transition([0], [1])
    p = PetriNet([t])
    s1 = State([5,0], p)
    prop = EUProposition(LessProposition(NumericExpression(0),
    VariableExpression(0)), EqualsProposition(VariableExpression(1), NumericExpression(3)))
    p = PropContinuation(prop, EndContinuation(True), EndContinuation(False))
    assert run(p, s1) == True

def test_mark_continuation_true():
    p = TrueProposition()
    prop = PropContinuation(p, EndContinuation(True), EndContinuation(False))
    s1 = State([1])
    assert run(prop, s1) == True
    assert s1.labels[p.label()] == True

def test_mark_continuation_false():
    p = FalseProposition()
    prop = PropContinuation(p, EndContinuation(True), EndContinuation(False))
    s1 = State([1])
    assert run(prop, s1) == False
    assert s1.labels[p.label()] == False
def test_eg_continuation1():
    net, state = parse_net("""
P:7
T:0->1
T:0->2
T:0->3
T:0->4
T:0->5
T:0->6
S:1|0|0|0|0|0|0
""")
    prop = parse_props('EG true')[0]
    prop1 = parse_props('EG false')[0]
    cont = PropContinuation(prop, EndContinuation(True), EndContinuation(False))
    cont1 = PropContinuation(prop1, EndContinuation(True), EndContinuation(False))
    assert run(cont, state) == True
    assert run(cont1, state) == False

def test_eg_continuation2():
    net, state = parse_net("""
P:5
T:0->1
T:0->2
T:1->3
T:2->4
S:1|0|0|0|0""")
    prop = parse_props('EG $4=0')[0]
    cont = PropContinuation(prop, EndContinuation(True), EndContinuation(False))
    assert run(cont, state) == False

def test_ex_continuation():
    net, state = parse_net("""
P:7
T:0->1
T:0->2
T:0->3
T:0->4
T:0->5
T:0->6
S:1|0|0|0|0|0|0
""")
    prop = parse_props('EX $5 = 1')[0]
    cont = PropContinuation(prop, EndContinuation(True), EndContinuation(False))
    assert run(cont, state) == True


def test_eu_continuation():
    net, state = parse_net("""
P:7
T:0->1
T:0->2
T:0->3
T:0->4
T:0->5
T:0->6
S:1|0|0|0|0|0|0
""")
    prop = parse_props('E true U $6 = 1')[0]
    prop1 = parse_props('E true U $6 = 1')[0]
    cont = PropContinuation(prop, EndContinuation(True), EndContinuation(False))
    assert run(cont, state) == True

def run(cont, state):
    while not cont.is_done():
        cont, f, state = cont.activate(state)
    assert isinstance(cont, EndContinuation)
    return cont.result
