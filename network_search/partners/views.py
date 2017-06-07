from django.views.generic import DetailView

from network_search.core.views import SearchView
from network_search.partners.forms import PartnerSearchForm
from network_search.partners.models import Partner


class PartnerView(DetailView):
    queryset = Partner.partners.active()
    template_name = "partners/partner_detail.html"


class PartnerSearchView(SearchView):
    """
    List and search for partners
    """
    context_object_name = "partners"
    form_class = PartnerSearchForm
    queryset = Partner.partners.active()
    template_name = "partners/partner_list.html"

