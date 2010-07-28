from parse import parse_net
from petri_net import PetriNet

def test_parse():
    net = """P: 2
T: 0|1 -> 0|1
T: 0 -> 1
"""
    pnet = parse_net(net)
    assert isinstance(pnet, PetriNet)
    assert len(pnet.transitions) == 2
    t0 = pnet.transitions[0]
    assert t0.input == [0,1]
    assert t0.output == [0,1]
    t1 = pnet.transitions[1]
    assert t1.input == [0]
    assert t1.output == [1]
