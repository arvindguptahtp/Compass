"""
Tests for loading the views
"""

import pytest
from django.core.urlresolvers import reverse

from network_search.core.views import HomePage
from network_search.partners.views import PartnerSearchView
from network_search.programs.views import ProgramSearchView
from network_search.affiliates.views import AffiliateSearchView

non_detail_urls = [
    ('home', HomePage),
    ('affiliate_list', AffiliateSearchView),
    ('partner_list', PartnerSearchView),
    ('program_list', ProgramSearchView),
]


@pytest.mark.django_db
@pytest.mark.parametrize("url_name,view", non_detail_urls)
def test_protected_access(url_name, view, client):
    response = client.get(reverse(url_name))
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize("url_name,view", non_detail_urls)
def test_list_views_load(url_name, view, rf):

    request = rf.get(url_name)
    request.session = {'simple_auth': True}

    response = view.as_view()(request)
    assert response.status_code == 200
