from transition import Transition
from state import State

def test_transition():
    t = Transition(input=[1], output=[])
    assert t.input == [1]
    assert t.output == []

def test_no_input_transition():
    t = Transition([], [0])
    state = State([4])
    s2 = t.fire(state)
    assert s2.tokens == [5]

def test_no_output_transition():
    t = Transition([0], [])
    state = State([6])
    s2 = t.fire(state)
    assert s2.tokens == [5]

def test_nothing_transition():
    t = Transition([], [])
    state = State([6])
    s2 = t.fire(state)
    assert s2.tokens == [6]

def test_in_and_out_transition():
    t = Transition([0], [1])
    state = State([6, 5])
    s2 = t.fire(state)
    assert s2.tokens == [5, 6]

def test_loop():
    t = Transition([0], [0])
    state = State([6])
    s2 = t.fire(state)
    assert s2.tokens == [6]

def test_multi_in_out():
    t = Transition([0, 1, 2, 3], [4, 5, 6])
    state = State([1, 2, 3, 4, 0, 1, 2])
    s2 = t.fire(state)
    assert s2.tokens == [0, 1, 2, 3, 1, 2, 3]

def test_transition_can_fire():
    t = Transition([], [])
    assert t.can_fire(State([0])) == True
    t1 = Transition([], [0])
    assert t1.can_fire(State([6])) == True
    t2 = Transition([0], [])
    assert t2.can_fire(State([1])) == True
    t3 = Transition([0],[])
    assert t3.can_fire(State([0])) == False
    t4 = Transition([0, 1], [])
    assert t4.can_fire(State([320, 0])) == False


