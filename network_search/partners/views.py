from django.views.generic import DetailView

from network_search.core.views import PDFMixin
from network_search.core.views import SearchView
from network_search.partners.forms import PartnerSearchForm
from network_search.partners.models import Partner


class PartnerView(DetailView):
    queryset = Partner.partners.active()
    template_name = "partners/partner_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'org_type': 'Partner',
        })
        return context


class PartnerPDFView(PDFMixin, PartnerView):
    template_name = "partners/partner_pdf.html"
    base_url = "http://localhost:8000/"


class PartnerSearchView(SearchView):
    """
    List and search for partners
    """
    context_object_name = "partners"
    form_class = PartnerSearchForm
    queryset = Partner.partners.active()
    template_name = "partners/partner_list.html"
