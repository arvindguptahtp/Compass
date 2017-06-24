"""
Tests for
"""
import pytest

from network_search.core import choices
from network_search.tests.fixtures import affiliate_factory
from network_search.tests.fixtures import school_data_factory
from network_search.affiliates.models import AffiliateEOYData


def test_school_districts():
    affiliate = AffiliateEOYData(districts="City of Fun, Town of Boring, County of Learning")
    assert affiliate.school_districts_count == 3
    assert affiliate.school_districts == ["City of Fun", "Town of Boring", "County of Learning"]


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
    school_data = school_data_factory(
        affiliate=affiliate,
        year=current_eoy,
    )
    affiliate_data = AffiliateEOYData.objects.get(pk=school_data.affiliate_data.pk)

    assert 0 == affiliate_data.total_students_frpl()
    assert 0 == affiliate_data.total_students_adjudicated_youth()
    assert 0 == affiliate_data.total_students_child_of_military()
    assert 0 == affiliate_data.total_students_ell()
    assert 0 == affiliate_data.total_students_foster()
    assert 0 == affiliate_data.total_students_gang()
    assert 0 == affiliate_data.total_students_homeless()
    assert 0 == affiliate_data.total_students_incarcerated_parent()
    assert 0 == affiliate_data.total_students_lgbt()
    assert 0 == affiliate_data.total_students_pregnant_parenting()
    assert 0 == affiliate_data.total_students_special_education()
    assert 0 == affiliate_data.total_students_substance_abuse()
