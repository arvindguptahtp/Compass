"""
Tests for searching partners
"""

import pytest

from network_search.affiliates.models import Affiliate
from network_search.core.choices import CoreServices
from network_search.core.choices import Gender
from network_search.core.choices import Grades
from network_search.core.choices import Regions
from network_search.core.choices import Setting
from network_search.core.choices import StudentNeeds
from network_search.core.choices import TiersOfEvidence
from network_search.core.choices import TiersOfService
from network_search.partners.forms import PartnerSearchForm
from network_search.partners.models import Partner


@pytest.fixture
def base_affiliate():
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
def empty_partner():
    yield Partner.partners.create(name="Empty")


@pytest.fixture
def girl_scouts():
    yield Partner.partners.create(
        name="Girl Scouts",
        gender=[Gender.f.name],
        grade=[Grades.el.name],
        student_need=[StudentNeeds.bi.name],
        organizational_reach=[Regions.n.name],
        tiers_of_service=[TiersOfService.i.name],
        setting=[Setting.aft.name],
        service_categories=[CoreServices.aa.name],
        tiers_of_evidence=[TiersOfEvidence.t1.name],
        is_cost_free=True,
    )


@pytest.fixture
def boy_scouts():
    yield Partner.partners.create(
        name="Boy Scouts",
        gender=[Gender.m.name],
        grade=[Grades.ms.name],
        student_need=[StudentNeeds.att.name],
        organizational_reach=[Regions.i.name],
        tiers_of_service=[TiersOfService.ii.name],
        setting=[Setting.sch.name],
        service_categories=[CoreServices.bi.name],
        tiers_of_evidence=[TiersOfEvidence.t2.name],
        is_cost_free=False,
    )


@pytest.fixture
def girls_and_boys_club():
    yield Partner.partners.create(
        name="Girls and Boys Club",
        gender=Gender.all_names(),
        grade=Grades.all_names(),
        student_need=StudentNeeds.all_names(),
        organizational_reach=Regions.all_names(),
        tiers_of_service=TiersOfService.all_names(),
        setting=Setting.all_names(),
        service_categories=CoreServices.all_names(),
        tiers_of_evidence=TiersOfEvidence.all_names(),
        is_cost_free=True,
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


@pytest.mark.django_db
def test_search_student_need(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={'need': [StudentNeeds.bi.name]})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'need': [StudentNeeds.att.name]})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'need': [StudentNeeds.bi.name, StudentNeeds.att.name]})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'need': []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_reach(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={'reach': [Regions.n.name]})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'reach': [Regions.i.name]})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'reach': [Regions.n.name, Regions.i.name]})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'reach': []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_tiers_of_services(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={'service_tiers': [TiersOfService.i.name]})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'service_tiers': [TiersOfService.ii.name]})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'service_tiers': [TiersOfService.i.name, TiersOfService.ii.name]})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'service_tiers': []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_setting(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={'setting': [Setting.aft.name]})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'setting': [Setting.sch.name]})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'setting': [Setting.aft.name, Setting.sch.name]})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'setting': []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_service_categories(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={"services": [CoreServices.aa.name]})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={"services": [CoreServices.bi.name]})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={"services": [CoreServices.aa.name, CoreServices.bi.name]})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={"services": []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_evidence(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={'evidence': [TiersOfEvidence.t1.name]})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'evidence': [TiersOfEvidence.t2.name]})
    assert form.is_valid()
    assert {boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'evidence': [TiersOfEvidence.t1.name, TiersOfEvidence.t2.name]})
    assert form.is_valid()
    assert {girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'evidence': []})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_cost(empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    form = PartnerSearchForm(data={'free_of_cost': True})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'free_of_cost': False})
    assert form.is_valid()
    assert {boy_scouts, empty_partner} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'free_of_cost': None})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa


@pytest.mark.django_db
def test_search_in_network(base_affiliate, empty_partner, girl_scouts, boy_scouts, girls_and_boys_club):

    girl_scouts.network_use.add(base_affiliate)
    girls_and_boys_club.network_use.add(base_affiliate)

    assert Partner.partners.filter(network_use=True).exists()

    form = PartnerSearchForm(data={'use_in_network': True})
    assert form.is_valid()
    assert {girl_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'use_in_network': False})
    assert form.is_valid()
    assert {boy_scouts, empty_partner} == set(Partner.partners.search(**form.cleaned_data))

    form = PartnerSearchForm(data={'use_in_network': None})
    assert form.is_valid()
    assert {empty_partner, girl_scouts, boy_scouts, girls_and_boys_club} == set(Partner.partners.search(**form.cleaned_data))  # noqa
