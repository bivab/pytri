import py

from place import Place

def test_place():
    p = Place()
    assert p.tokens == 0
    p = Place(12345)
    assert p.tokens == 12345

def test_no_negative_tokens():
    assert py.test.raises(ValueError, 'Place(-1)')
