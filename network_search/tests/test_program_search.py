"""
Tests for searching programs
"""

import pytest

from network_search.core.choices import Race
from network_search.core.choices import Gender
from network_search.core.choices import CoreServices
from network_search.core.choices import StudentNeeds
from network_search.core.choices import TiersOfService
from network_search.core.choices import AffiliateGrades
from network_search.core.choices import TiersOfEvidence
from network_search.programs.forms import ProgramSearchForm
from network_search.programs.models import Program
from network_search.affiliates.models import Affiliate


@pytest.fixture
def program_affiliate():
    yield Affiliate.affiliates.create(
        name="Base Affiliate",
        state="VA",
        cis_id=8,
        official_name="Base Affiliate",
        address_street="100 Main St",
        address_city="Anywhere",
        address_state="VA",
        address_postcode="22202",
    )


@pytest.fixture
def gs_program():
    yield Program.programs.create(
        name="Girl Scouts",
        gender=[Gender.f.name],
        grade=[AffiliateGrades.el.name],
        race=[Race.am.name],
        student_need=[StudentNeeds.bi.name],
        tiers_of_service=[TiersOfService.i.name],
        service_categories=[CoreServices.aa.name],
        tiers_of_evidence=[TiersOfEvidence.t1.name],
        is_cost_free=True,
    )


@pytest.fixture
def bsa_program():
    yield Program.programs.create(
        name="Boy Scouts",
        gender=[Gender.m.name],
        grade=[AffiliateGrades.ms.name],
        race=[Race.asn.name],
        student_need=[StudentNeeds.att.name],
        tiers_of_service=[TiersOfService.ii.name],
        service_categories=[CoreServices.bi.name],
        tiers_of_evidence=[TiersOfEvidence.t2.name],
        is_cost_free=False,
    )


@pytest.fixture
def girls_boys_club_program():
    yield Program.programs.create(
        name="Girls and Boys Club",
        gender=Gender.all_names(),
        grade=AffiliateGrades.all_names(),
        race=[Race.am.name, Race.asn.name],
        student_need=StudentNeeds.all_names(),
        tiers_of_service=TiersOfService.all_names(),
        service_categories=CoreServices.all_names(),
        tiers_of_evidence=TiersOfEvidence.all_names(),
        is_cost_free=True,
    )


@pytest.mark.django_db
def test_search_gender(empty_program, gs_program, bsa_program, girls_boys_club_program):

    form = ProgramSearchForm(data={'gender': [Gender.f.name]})
    assert form.is_valid()
    assert {gs_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'gender': [Gender.m.name]})
    assert form.is_valid()
    assert {bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'gender': [Gender.f.name, Gender.m.name]})
    assert form.is_valid()
    assert {gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa

    form = ProgramSearchForm(data={'gender': []})
    assert form.is_valid()
    assert {empty_program, gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_grade(empty_program, gs_program, bsa_program, girls_boys_club_program):

    form = ProgramSearchForm(data={'grade': [AffiliateGrades.el.name]})
    assert form.is_valid()
    assert {gs_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'grade': [AffiliateGrades.ms.name]})
    assert form.is_valid()
    assert {bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'grade': [AffiliateGrades.el.name, AffiliateGrades.ms.name]})
    assert form.is_valid()
    assert {gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa

    form = ProgramSearchForm(data={'grade': []})
    assert form.is_valid()
    assert {empty_program, gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_race(empty_program, gs_program, bsa_program, girls_boys_club_program):

    form = ProgramSearchForm(data={'race': [Race.am.name]})
    assert form.is_valid()
    assert {gs_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'race': [Race.asn.name]})
    assert form.is_valid()
    assert {bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'race': [Race.am.name, Race.asn.name]})
    assert form.is_valid()
    assert {gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa

    form = ProgramSearchForm(data={'race': []})
    assert form.is_valid()
    assert {empty_program, gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_student_need(empty_program, gs_program, bsa_program, girls_boys_club_program):

    form = ProgramSearchForm(data={'need': [StudentNeeds.bi.name]})
    assert form.is_valid()
    assert {gs_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'need': [StudentNeeds.att.name]})
    assert form.is_valid()
    assert {bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'need': [StudentNeeds.bi.name, StudentNeeds.att.name]})
    assert form.is_valid()
    assert {gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa

    form = ProgramSearchForm(data={'need': []})
    assert form.is_valid()
    assert {empty_program, gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_tiers_of_services(empty_program, gs_program, bsa_program, girls_boys_club_program):

    form = ProgramSearchForm(data={'service_tiers': [TiersOfService.i.name]})
    assert form.is_valid()
    assert {gs_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'service_tiers': [TiersOfService.ii.name]})
    assert form.is_valid()
    assert {bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'service_tiers': [TiersOfService.i.name, TiersOfService.ii.name]})
    assert form.is_valid()
    assert {gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa

    form = ProgramSearchForm(data={'service_tiers': []})
    assert form.is_valid()
    assert {empty_program, gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_service_categories(empty_program, gs_program, bsa_program, girls_boys_club_program):

    form = ProgramSearchForm(data={"services": [CoreServices.aa.name]})
    assert form.is_valid()
    assert {gs_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={"services": [CoreServices.bi.name]})
    assert form.is_valid()
    assert {bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={"services": [CoreServices.aa.name, CoreServices.bi.name]})
    assert form.is_valid()
    assert {gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa

    form = ProgramSearchForm(data={"services": []})
    assert form.is_valid()
    assert {empty_program, gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_evidence(empty_program, gs_program, bsa_program, girls_boys_club_program):

    form = ProgramSearchForm(data={'evidence': [TiersOfEvidence.t1.name]})
    assert form.is_valid()
    assert {gs_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'evidence': [TiersOfEvidence.t2.name]})
    assert form.is_valid()
    assert {bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'evidence': [TiersOfEvidence.t1.name, TiersOfEvidence.t2.name]})
    assert form.is_valid()
    assert {gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa

    form = ProgramSearchForm(data={'evidence': []})
    assert form.is_valid()
    assert {empty_program, gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_cost(empty_program, gs_program, bsa_program, girls_boys_club_program):

    form = ProgramSearchForm(data={'free_of_cost': True})
    assert form.is_valid()
    assert {gs_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'free_of_cost': False})
    assert form.is_valid()
    assert {bsa_program, empty_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'free_of_cost': None})
    assert form.is_valid()
    assert {empty_program, gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa


@pytest.mark.skip("Passes run individually but not in the suite...")
@pytest.mark.django_db
def test_search_in_network(program_affiliate, empty_program, gs_program, bsa_program, girls_boys_club_program):

    gs_program.network_use.add(program_affiliate)
    girls_boys_club_program.network_use.add(program_affiliate)

    assert gs_program.network_use.all().count() == 1
    assert girls_boys_club_program.network_use.all().count() == 1

    assert Program.programs.get(pk=gs_program.pk).network_use.all().count() == 1

    assert Program.programs.exclude(network_use=False).count() == 2
    assert Program.programs.filter(network_use=True).exists()

    form = ProgramSearchForm(data={'use_in_network': True})
    assert form.is_valid()
    assert {gs_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'use_in_network': False})
    assert form.is_valid()
    assert {bsa_program, empty_program} == set(Program.programs.search(**form.cleaned_data))

    form = ProgramSearchForm(data={'use_in_network': None})
    assert form.is_valid()
    assert {empty_program, gs_program, bsa_program, girls_boys_club_program} == set(Program.programs.search(**form.cleaned_data))  # noqa
