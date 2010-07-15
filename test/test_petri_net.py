from petri_net import PetriNet
from place import Place
from state import State
from transition import Transition

def test_petri_net():
    p = PetriNet([])
    assert p.transitions == []
    t1, t2 = [Transition([],[]), Transition([], [])]
    p1 = PetriNet([t1, t2])
    assert p1.transitions == [t1, t2]

def test_petri_net_enabled_transitions():
    t1 = Transition([Place(10)], [])
    t2 = Transition([Place(0)], [Place(12312312)])
    p = PetriNet([t1,t2])
    assert p.enabled_transitions() == [t1]

def test_petri_net_state():
    t1 = Transition([Place(10)], [])
    t2 = Transition([Place(0)], [Place(12312312)])
    p = PetriNet([t1,t2])
    assert p.state() == State([10, 0, 12312312])

def test_petri_net_computes_places():
    p1, p2, p3, p4 = [Place(10), Place(10), Place(0), Place(12312312)]
    t1 = Transition([p1], [p2])
    t2 = Transition([p3], [p4])
    p = PetriNet([t1,t2])
    places = p.get_places()
    assert p1 in places
    assert p2 in places
    assert p3 in places
    assert p4 in places
