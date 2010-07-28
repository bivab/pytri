from parse import parse_net, parse_props
from petri_net import PetriNet
from propositions import EGProposition, TrueProposition, EUProposition, EXProposition, FalseProposition
from propositions import NegationProposition, AndProposition, EqualsProposition, LessProposition, OrProposition
from expression import VariableExpression, NumericExpression

def test_parse_petri_net():
    net = """P: 2
T: 0|1 -> 0|1
T: 0 -> 1
S:123|5345
"""
    pnet,state = parse_net(net)
    assert isinstance(pnet, PetriNet)
    assert len(pnet.transitions) == 2
    t0 = pnet.transitions[0]
    assert t0.input == [0,1]
    assert t0.output == [0,1]
    t1 = pnet.transitions[1]
    assert t1.input == [0]
    assert t1.output == [1]
    assert state.tokens == [123, 5345]

def test_parse_ctl():
    ctls = parse_props("""EG true
EX false
E true U false
EX true & not false
EG not(false & not true )
EG $1 < 100 & 0 = $1
EX true | false""")

    assert ctls[0] == EGProposition(TrueProposition())
    assert ctls[1] == EXProposition(FalseProposition())
    assert ctls[2] == EUProposition(TrueProposition(), FalseProposition())
    assert ctls[3] == EXProposition(AndProposition(TrueProposition(), NegationProposition(FalseProposition())))
    assert ctls[4] == EGProposition(NegationProposition(AndProposition(FalseProposition(), NegationProposition(TrueProposition()))))
    assert ctls[5] == EGProposition(AndProposition(LessProposition(VariableExpression(1), NumericExpression(100)), EqualsProposition(NumericExpression(0), VariableExpression(1))))
    assert ctls[6] == EXProposition(OrProposition(TrueProposition(), FalseProposition()))
