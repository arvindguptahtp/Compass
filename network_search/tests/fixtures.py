"""

"""
import pytest

from network_search.partners.models import Partner
from network_search.programs.models import Program
from network_search.affiliates.models import Affiliate
from network_search.affiliates.models import EndOfYear
from network_search.affiliates.models import SchoolEOYData
from network_search.affiliates.models import AffiliateEOYData


def affiliate_factory(**kwargs):
    defaults = dict(
        name="Base Affiliate",
        state="VA",
        cis_id=8,
        official_name="Base Affiliate",
        address_street="100 Main St",
        address_city="Anywhere",
        address_state="VA",
        address_postcode="22202",
    )
    defaults.update(kwargs)
    return Affiliate.affiliates.create(**defaults)


def school_data_factory(affiliate, year, **kwargs):
    defaults = dict(
        students_female_american_indian=0,
        students_female_asian=0,
        students_female_black=0,
        students_female_hispanic=0,
        students_female_white=0,
        students_female_two_or_more_races=0,
        students_female_other=0,
        students_female_unknown=0,
        students_male_american_indian=0,
        students_male_asian=0,
        students_male_black=0,
        students_male_hispanic=0,
        students_male_white=0,
        students_male_two_or_more_races=0,
        students_male_other=0,
        students_male_unknown=0,
        students_unknown_race_gender=0,
        students_served_frpl=0,
        students_served_ell=0,
        students_served_foster=0,
        students_served_homeless=0,
        students_served_lgbt=0,
        students_served_pregnant_parenting=0,
        students_served_special_education=0,
        students_served_substance_abuse=0,
        students_served_adjudicated_youth=0,
        students_served_child_of_military=0,
        students_served_gang=0,
        students_served_incarcerated_parent=0,
    )
    defaults.update(kwargs)
    affiliate_data, _ = AffiliateEOYData.objects.get_or_create(affiliate=affiliate, year=year)
    defaults.update({'affiliate_data': affiliate_data})
    school_data = SchoolEOYData.objects.create(**defaults)
    return school_data


@pytest.fixture
def current_eoy():
    yield EndOfYear.objects.create(year_ends=2017, is_active=True)


@pytest.fixture
def past_eoy():
    yield EndOfYear.objects.create(year_ends=2016, is_active=False)


@pytest.fixture
def empty_partner():
    yield Partner.partners.create(name="Empty")


@pytest.fixture
def affiliate_data(current_eoy):
    affiliate = affiliate_factory()
    school = school_data_factory(affiliate, current_eoy)
    yield {
        "affiliate": affiliate,
        "school": school,
        "affiliate_data": school.affiliate_data,
    }


@pytest.fixture
def empty_program():
    yield Program.programs.create(name="Empty")


@pytest.fixture
def base_affiliate():
    yield affiliate_factory()
