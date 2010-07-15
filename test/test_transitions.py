from transition import Transition
from place import Place
def test_transition():
    t = Transition(input=[1], output=[])
    assert t.input == [1]
    assert t.output == []

def test_no_input_transition():
    p = Place(4)
    t = Transition([], [p])
    t.fire()
    assert p.tokens == 5

def test_no_output_transition():
    p = Place(4)
    t = Transition([p], [])
    t.fire()
    assert p.tokens == 3

def test_nothing_transition():
    t = Transition([], [])
    t.fire()
    assert t.input == []
    assert t.output == []

def test_in_and_out_transition():
    in_p = Place(3)
    out_p = Place(4234)
    t = Transition([in_p], [out_p])
    t.fire()
    assert in_p.tokens == 2
    assert out_p.tokens == 4235

def test_loop():
    in_out_p = Place(42)
    t = Transition([in_out_p], [in_out_p])
    t.fire()
    assert in_out_p.tokens == 42

def test_multi_in_out():
    inp = [Place(i) for i in range(1, 5)]
    out = [Place(i) for i in range(3)]
    t = Transition(inp, out)
    t.fire()
    for i in range(4):
        assert inp[i].tokens == i
    for i in range(1, 4):
        assert out[i-1].tokens == i

def test_transition_can_fire():
    t = Transition([], [])
    assert t.can_fire() == True
    t1 = Transition([], [1])
    assert t1.can_fire() == True
    t2 = Transition([Place(1)], [])
    assert t2.can_fire() == True
    t3 = Transition([Place(0)],[])
    assert t3.can_fire() == False
    t4 = Transition([Place(320), Place(0)], [])
    assert t4.can_fire() == False


