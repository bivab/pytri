from state import State
from propositions import LessProposition

def test_less_than():
    state = State([2,0,0,1,0])
    assert state.eval_prop(LessProposition(state.get(3), state.get(0))) == True
    assert state.eval_prop(LessProposition(state.get(0), state.get(3))) == False

    assert state.eval_prop(LessProposition(123412, state.get(3))) == False
    assert state.eval_prop(LessProposition(-1, state.get(3))) == True
