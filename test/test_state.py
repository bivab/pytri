from state import State
def test_state_hash():
    s = State([1,2,3,4])
    assert hash(s) == s.hash()

