from animator import Animator
from petri_net import PetriNet
from state import State
from transition import Transition

def test_animator():
    state = State([0,0,0])
    t1 = Transition([], [0])
    t2 = Transition([0], [1])
    t3 = Transition([0], [2])
    net = PetriNet([t1,t2,t3])
    tr1 = net.enabled_transitions(state)
    assert tr1 == [t1]
    result = tr1[0].fire(state)
    tr2 = net.enabled_transitions(result)
    assert tr2 == [t1, t2, t3]

def test_animator2():
    t1 = Transition([], [0])
    t2 = Transition([0], [1])
    t3 = Transition([0], [2])
    net = PetriNet([t1,t2,t3])
    state = State([0,0,0], net)
    a = Animator(net, state)
    assert a.stack == [state]
    a.step()
    assert a.stack == [State([1,0,0])]
    assert state._successors == a.stack
    a.step()
    assert a.stack == [State([2,0,0]), State([0,1,0]), State([0,0,1])]

def test_animator_run():
    state = State([2,0,0,1,0])
    t1 = Transition([0], [1])
    t2 = Transition([1,3], [2])
    t3 = Transition([2], [3, 4])
    t4 = Transition([4], [0])
    net = PetriNet([t1,t2,t3,t4])
    a = Animator(net, state)
    a.run()
    assert len(a.states) == 9

