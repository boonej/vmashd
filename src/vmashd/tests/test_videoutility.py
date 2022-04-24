import vmashd.videoutility as vu


def test_roll():
    r = vu.roll()
    assert(r < 101)
    assert(r > -1)
    assert(isinstance(r, int))
