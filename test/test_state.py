from state import State, state_hash
def test_state_hash():
    s = State([1,2,3,4])
    assert hash(s) == state_hash(s)

