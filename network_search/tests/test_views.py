"""
Tests for loading the views
"""

import pytest
from django.core.urlresolvers import reverse

from network_search.core.views import HomePage
from network_search.partners.views import PartnerView
from network_search.partners.views import PartnerPDFView
from network_search.partners.views import PartnerSearchView
from network_search.programs.views import ProgramView
from network_search.programs.views import ProgramPDFView
from network_search.programs.views import ProgramSearchView
from network_search.affiliates.views import AffiliateView
from network_search.affiliates.views import AffiliatePDFView
from network_search.affiliates.views import AffiliateSearchView

non_detail_urls = [
    ('home', HomePage),
    ('affiliate_list', AffiliateSearchView),
    ('partner_list', PartnerSearchView),
    ('program_list', ProgramSearchView),
]

affiliate_urls = [
    ('affiliate_detail', AffiliateView),
    ('affiliate_pdf', AffiliatePDFView),
]

partner_urls = [
    ('partner_detail', PartnerView),
    ('partner_pdf', PartnerPDFView),
]

program_urls = [
    ('program_detail', ProgramView),
    ('program_pdf', ProgramPDFView),
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


@pytest.mark.django_db
@pytest.mark.parametrize("url_name,view", affiliate_urls)
def test_affiliate_views(url_name, view, affiliate_data, rf):
    """Ensure affiliate detail/pdf view load successfully"""
    affiliate = affiliate_data['affiliate']
    request = rf.get(url_name, {"pk": affiliate.pk})
    request.session = {'simple_auth': True}
    if 'pdf' in url_name:
        response = view.as_view()(request, pk=affiliate.pk)
    else:
        response = view.as_view()(request, pk=affiliate.pk).render()
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("url_name,view", partner_urls)
def test_partner_views(url_name, view, empty_partner, rf):
    """Ensure partner detail/pdf view load successfully"""
    request = rf.get(url_name, {"pk": empty_partner.pk})
    request.session = {'simple_auth': True}
    if 'pdf' in url_name:
        response = view.as_view()(request, pk=empty_partner.pk)
    else:
        response = view.as_view()(request, pk=empty_partner.pk).render()
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("url_name,view", program_urls)
def test_program_views(url_name, view, empty_program, rf):
    """Ensure program detail/pdf view load successfully"""
    request = rf.get(url_name, {"pk": empty_program.pk})
    request.session = {'simple_auth': True}
    if 'pdf' in url_name:
        response = view.as_view()(request, pk=empty_program.pk)
    else:
        response = view.as_view()(request, pk=empty_program.pk).render()
    assert response.status_code == 200
