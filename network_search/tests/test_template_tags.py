import pytest

from network_search.core import choices
from network_search.core.templatetags import choice_tags


def test_choice_display():
    assert choice_tags.choice_display("m", "Gender") == choices.Gender.m.value


def test_bad_choice_enum():
    """If specified enum class doesn't exist raise an error"""
    with pytest.raises(AttributeError):
        choice_tags.choice_display("m", "WillyWonka")


def test_bad_name():
    """If the name doesn't exist on the choice enum, return original value"""
    assert choice_tags.choice_display("z", "Gender") == "z"


def test_choice_tag_template():
    tmpl = "{% load choice_tags %} {{ g|choice_display:Gender }}"
