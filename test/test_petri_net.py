from petri_net import PetriNet
from state import State
from transition import Transition

def test_petri_net():
    p = PetriNet([])
    assert p.transitions == []
    t1, t2 = [Transition([],[]), Transition([], [])]
    p1 = PetriNet([t1, t2])
    assert p1.transitions == [t1, t2]

def test_petri_net_enabled_transitions():
    t1 = Transition([0], [])
    t2 = Transition([1], [2])
    p = PetriNet([t1,t2])
    assert p.enabled_transitions(State([1, 0, 0])) == [t1]

def test_petri_net_caches_state():
    t1 = Transition([0], [])
    t2 = Transition([1], [2])
    p = PetriNet([t1,t2])
    assert p.state([0, 1, 2]) is p.state([0, 1, 2])
