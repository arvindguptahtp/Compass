"""
Tests for searching partners
"""

import pytest

from network_search.partners.models import Partner


@pytest.fixture
def empty_partner():
    yield Partner.partners.create(name="Empty")


@pytest.fixture
def girl_scouts():
    yield Partner.partners.create(name="Girl Scouts", gender=['f'], grade=['el'])


@pytest.fixture
def boy_scouts():
    yield Partner.partners.create(name="Boy Scouts", gender=['m'], grade=['ms'])


@pytest.fixture
def girls_and_boys_club():
    yield Partner.partners.create(
        name="Girls and Boys Club",
        gender=['f', 'm'],
        grade=['el', 'ms']
    )


@pytest.mark.django_db
def test_search_gender(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(gender=['f']))
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(gender=['m']))
    assert {girls_and_boys_club} == set(Partner.partners.search(gender=['m', 'f']))
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(gender=[]))


@pytest.mark.django_db
def test_search_grade(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(grade=['el']))
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(grade=['ms']))
    assert {girls_and_boys_club} == set(Partner.partners.search(grade=['el', 'ms']))
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(grade=[]))
