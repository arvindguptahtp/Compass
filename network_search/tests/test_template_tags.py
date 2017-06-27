import pytest
from django import template

from network_search.core import choices
from network_search.core.templatetags import choice_tags
from network_search.core.templatetags import network_search_tags


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
    tmpl = template.Template("{% load choice_tags %}{{ g|choice_display:'Gender' }}")
    assert tmpl.render(template.Context({"g": "f"})).strip() == "female"


def test_us_state():
    assert network_search_tags.us_state("va") == "Virginia"
    assert network_search_tags.us_state("Va") == "Virginia"
    assert network_search_tags.us_state("VA") == "Virginia"
    assert network_search_tags.us_state("VX") == "VX"
    assert network_search_tags.us_state("vx") == "vx"


def test_state_tag_template():
    tmpl = template.Template("{% load network_search_tags %}{{ state|us_state }}")
    assert tmpl.render(template.Context({"state": "va"})).strip() == "Virginia"
