"""
Tests for application model methods
"""
import pytest

from network_search.core import choices
from network_search.tests.fixtures import affiliate_factory
from network_search.tests.fixtures import school_data_factory
from network_search.affiliates.models import Affiliate
from network_search.affiliates.models import AffiliateEOYData


def test_affiliate_location_display():
    affiliate = Affiliate(affiliate_location='S')
    assert affiliate.get_affiliate_location_display() == 'Suburban'


def test_school_districts():
    affiliate = AffiliateEOYData(districts="City of Fun, Town of Boring, County of Learning")
    assert affiliate.school_districts_count == 3
    assert affiliate.school_districts == ["City of Fun", "Town of Boring", "County of Learning"]


def test_affiliate_data_funding():
    affiliate_data = AffiliateEOYData(
        funding_public_federal=1000,
        funding_public_state=1000,
        funding_public_city=100,
        funding_public_school_district=100,
        funding_private_corporate=200,
        funding_private_foundation=20,
        funding_private_board=20,
        funding_private_individual=20,
        funding_private_events=20,
        funding_private_cis_national=20,
        funding_private_cis_state_office=20,
        funding_private_npo=20,
        funding_private_other=20,
    )

    assert affiliate_data.funding_public == 2200
    assert affiliate_data.funding_private == 360


@pytest.mark.django_db
def test_gender_data(current_eoy):
    affiliate = affiliate_factory()
    school_data_1 = school_data_factory(
        affiliate=affiliate,
        year=current_eoy,
        name="School 1",
        students_female_hispanic=4,
    )
    school_data_2 = school_data_factory(
        affiliate=affiliate,
        year=current_eoy,
        name="School 2",
        students_male_hispanic=1,
        students_female_hispanic=1,
        students_male_asian=1,
    )

    affiliate_data = AffiliateEOYData.objects.get(pk=school_data_2.affiliate_data.pk)
    assert affiliate_data == school_data_1.affiliate_data == school_data_2.affiliate_data

    assert affiliate_data.search_students_female == 5
    assert affiliate_data.search_students_male == 2
    assert set(affiliate_data.search_gender) == set(choices.Gender.all_names())


@pytest.mark.django_db
def test_affiliate_eoy_aggregation_methods(current_eoy):
    affiliate = affiliate_factory()
    school_data_1 = school_data_factory(
        affiliate=affiliate,
        year=current_eoy,
        students_served_frpl=1,
        students_served_ell=1,
        students_served_foster=1,
        students_served_homeless=1,
        students_served_lgbt=1,
        students_served_pregnant_parenting=1,
        students_served_special_education=1,
        students_served_substance_abuse=1,
        students_served_adjudicated_youth=1,
        students_served_child_of_military=1,
        students_served_gang=1,
        students_served_incarcerated_parent=1,
        students_total=340,
    )
    school_data_factory(
        affiliate=affiliate,
        year=current_eoy,
        students_served_frpl=2,
        students_served_ell=2,
        students_served_foster=2,
        students_served_homeless=2,
        students_served_lgbt=2,
        students_served_pregnant_parenting=2,
        students_served_special_education=2,
        students_served_substance_abuse=2,
        students_served_adjudicated_youth=2,
        students_served_child_of_military=2,
        students_served_gang=2,
        students_served_incarcerated_parent=2,
        students_total=200,
    )
    affiliate_data = AffiliateEOYData.objects.get(pk=school_data_1.affiliate_data.pk)

    assert 3 == affiliate_data.total_students_frpl()
    assert 3 == affiliate_data.total_students_adjudicated_youth()
    assert 3 == affiliate_data.total_students_child_of_military()
    assert 3 == affiliate_data.total_students_ell()
    assert 3 == affiliate_data.total_students_foster()
    assert 3 == affiliate_data.total_students_gang()
    assert 3 == affiliate_data.total_students_homeless()
    assert 3 == affiliate_data.total_students_incarcerated_parent()
    assert 3 == affiliate_data.total_students_lgbt()
    assert 3 == affiliate_data.total_students_pregnant_parenting()
    assert 3 == affiliate_data.total_students_special_education()
    assert 3 == affiliate_data.total_students_substance_abuse()

    assert 540 == affiliate_data.total_students_served()
