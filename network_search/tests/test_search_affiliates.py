"""
Tests for searching affiliates

This involves using data across multiple years and filtering only against
data for the current or most active reporting year.
"""

import pytest

from network_search.core.choices import Race
from network_search.core.choices import Gender
from network_search.tests.fixtures import affiliate_factory
from network_search.tests.fixtures import school_data_factory
from network_search.affiliates.forms import AffiliateSearchForm
from network_search.affiliates.models import Affiliate
from network_search.affiliates.models import EndOfYear
from network_search.affiliates.models import AffiliateEOYData

# TODO should an affiliate show up if no data for the latest reporting year?


@pytest.fixture
def base_affiliate():
    yield affiliate_factory()


@pytest.fixture
def local_affiliate():
    yield affiliate_factory(name="Local Affiliate", state="VA")


@pytest.fixture
def acme_affiliate():
    yield affiliate_factory(name="Acme", state="TX")


@pytest.fixture
def current_eoy():
    yield EndOfYear.objects.create(year_ends=2017, is_active=True)


@pytest.fixture
def past_eoy():
    yield EndOfYear.objects.create(year_ends=2016, is_active=False)


@pytest.fixture
def affiliate_universe(base_affiliate, local_affiliate, acme_affiliate, current_eoy, past_eoy):

    base_affiliate_old_data, _ = AffiliateEOYData.objects.get_or_create(year=past_eoy, affiliate=base_affiliate)
    base_affiliate_current_data, _ = AffiliateEOYData.objects.get_or_create(year=current_eoy, affiliate=base_affiliate)

    local_affiliate_old_data, _ = AffiliateEOYData.objects.get_or_create(year=past_eoy, affiliate=local_affiliate)
    local_affiliate_current_data, _ = AffiliateEOYData.objects.get_or_create(
        year=current_eoy, affiliate=local_affiliate)

    acme_affiliate_old_data, _ = AffiliateEOYData.objects.get_or_create(year=past_eoy, affiliate=acme_affiliate)
    acme_affiliate_current_data, _ = AffiliateEOYData.objects.get_or_create(year=current_eoy, affiliate=acme_affiliate)

    # This school has female and male students, black and asian in both years
    base_old_school_1 = school_data_factory(
        base_affiliate, past_eoy,
        students_female_asian=1, students_female_black=4,
        students_male_asian=1, students_male_black=4,
    )
    base_current_school_1 = school_data_factory(
        base_affiliate, current_eoy,
        students_female_asian=1, students_female_black=4,
        students_male_asian=1, students_male_black=4,
    )

    # This school has female and male students, black and asian in both years, white only in old year
    base_old_school_2 = school_data_factory(
        base_affiliate, past_eoy,
        students_female_asian=1, students_female_black=4, students_female_white=2,
        students_male_asian=1, students_male_black=4, students_male_white=2,
    )
    base_current_school_2 = school_data_factory(
        base_affiliate, current_eoy,
        students_female_asian=1, students_female_black=4,
        students_male_asian=1, students_male_black=4,
    )

    # Local affiliate has no male students in current year
    local_old_school_1 = school_data_factory(
        local_affiliate, past_eoy,
        students_female_asian=1, students_female_black=4,
        students_male_asian=1, students_male_black=4,
    )
    local_current_school_1 = school_data_factory(
        local_affiliate, current_eoy,
        students_female_asian=1, students_female_black=4,
        students_female_white=2, students_female_hispanic=3,
    )
    local_old_school_2 = school_data_factory(
        local_affiliate, past_eoy,
        students_female_asian=1, students_female_black=4,
        students_male_asian=1, students_male_black=4,
    )
    local_current_school_2 = school_data_factory(
        local_affiliate, current_eoy,
        students_female_asian=1, students_female_black=4,
    )

    yield [
        base_affiliate, local_affiliate, acme_affiliate, current_eoy, past_eoy,
        base_affiliate_current_data, base_affiliate_old_data,
        local_affiliate_current_data, local_affiliate_old_data,
        acme_affiliate_current_data, acme_affiliate_old_data,
        base_old_school_1, base_current_school_1, base_old_school_2, base_current_school_2,
        local_old_school_1, local_current_school_1, local_old_school_2, local_current_school_2,
    ]


@pytest.mark.django_db
def test_text_searching(affiliate_universe, acme_affiliate):
    form = AffiliateSearchForm(data={'q': "acme"})
    assert form.is_valid()
    assert {acme_affiliate} == set(Affiliate.affiliates.search(**form.cleaned_data))


@pytest.mark.django_db
def test_search_gender(affiliate_universe):

    form = AffiliateSearchForm(data={'gender': [Gender.f.name]})
    assert form.is_valid()
    results = Affiliate.affiliates.search(**form.cleaned_data)
    assert results.count() == 2

    form = AffiliateSearchForm(data={'gender': [Gender.m.name]})
    assert form.is_valid()
    results = Affiliate.affiliates.search(**form.cleaned_data)
    assert results.count() == 1

    form = AffiliateSearchForm(data={'gender': [Gender.f.name, Gender.m.name]})
    assert form.is_valid()
    results = Affiliate.affiliates.search(**form.cleaned_data)
    assert results.count() == 1

    form = AffiliateSearchForm(data={'gender': []})
    assert form.is_valid()
    results = Affiliate.affiliates.search(**form.cleaned_data)
    assert results.count() == 3


@pytest.mark.django_db
def test_search_race(affiliate_universe):

    form = AffiliateSearchForm(data={'race': [Race.am.name]})
    assert form.is_valid()
    results = Affiliate.affiliates.search(**form.cleaned_data)
    assert results.count() == 0

    form = AffiliateSearchForm(data={'race': [Race.his.name]})
    assert form.is_valid()
    results = Affiliate.affiliates.search(**form.cleaned_data)
    assert results.count() == 1

    form = AffiliateSearchForm(data={'race': [Race.asn.name]})
    assert form.is_valid()
    results = Affiliate.affiliates.search(**form.cleaned_data)
    assert results.count() == 2

    form = AffiliateSearchForm(data={'race': [Race.bl.name]})
    assert form.is_valid()
    results = Affiliate.affiliates.search(**form.cleaned_data)
    assert results.count() == 2

    form = AffiliateSearchForm(data={'race': [Race.asn.name, Race.bl.name]})
    assert form.is_valid()
    results = Affiliate.affiliates.search(**form.cleaned_data)
    assert results.count() == 2
