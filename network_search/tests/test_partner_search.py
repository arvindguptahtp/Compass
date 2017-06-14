"""
Tests for searching partners
"""

import pytest

from network_search.partners.forms import PartnerSearchForm
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

    form = PartnerSearchForm(data={'gender': ['f']})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'gender': ['m']})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'gender': ['f', 'm']})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'gender': []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_grade(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={'grade': ['el']})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'grade': ['ms']})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'grade': ['el', 'ms']})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'grade': []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa
