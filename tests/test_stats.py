from stats import average, maximum, minimum


def test_average():
    assert average([1, 2, 3]) == 2


def test_maximum():
    assert maximum([1, 5, 3]) == 5


def test_minimum():
    assert minimum([1, 5, 3]) == 1
