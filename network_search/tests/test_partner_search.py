"""
Tests for searching partners
"""

import pytest

from network_search.core.choices import Gender
from network_search.core.choices import Grades
from network_search.partners.forms import PartnerSearchForm
from network_search.partners.models import Partner


@pytest.fixture
def empty_partner():
    yield Partner.partners.create(name="Empty")


@pytest.fixture
def girl_scouts():
    yield Partner.partners.create(
        name="Girl Scouts",
        gender=[Gender.f.name],
        grade=[Grades.el.name],
        student_need=['bi'],
    )


@pytest.fixture
def boy_scouts():
    yield Partner.partners.create(
        name="Boy Scouts",
        gender=[Gender.m.name],
        grade=[Grades.ms.name],
        student_need=['att'],
    )


@pytest.fixture
def girls_and_boys_club():
    yield Partner.partners.create(
        name="Girls and Boys Club",
        gender=[Gender.f.name, Gender.m.name],
        grade=[Grades.el.name, Grades.ms.name],
        student_need=['bi', 'att'],
    )


@pytest.mark.django_db
def test_search_gender(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={'gender': [Gender.f.name]})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'gender': [Gender.m.name]})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'gender': [Gender.f.name, Gender.m.name]})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'gender': []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_grade(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={'grade': [Grades.el.name]})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'grade': [Grades.ms.name]})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'grade': [Grades.el.name, Grades.ms.name]})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'grade': []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa


@pytest.mark.skip
@pytest.mark.django_db
def test_search_student_need(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={'grade': [Grades.el.name]})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'grade': [Grades.ms.name]})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'grade': [Grades.el.name, Grades.ms.name]})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'grade': []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa
