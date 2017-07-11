from network_search.core import choices


def test_choice_populator():
    assert choices.populator(choices.Gender) == {'Female': 'f', 'Male': 'm'}
