
from network_search.core import choices


def test_choice_inversion():
    # Verify the test data looks as expected
    assert choices.GENDER == [('f', 'female'), ('m', 'male')]
    # Test it
    assert choices.inverted_choices(choices.GENDER) == [('female', 'f'), ('male', 'm')]


def test_choice_populator():
    # Verify the test data looks as expected
    assert choices.GENDER == [('f', 'female'), ('m', 'male')]
    # Test it
    assert choices.populator(choices.GENDER) == {'female': 'f', 'male': 'm'}
