from django.views.generic import DetailView

from network_search.affiliates.forms import AffiliateSearchForm
from network_search.affiliates.models import Affiliate
from network_search.core.views import PDFMixin
from network_search.core.views import SearchView


class AffiliateView(DetailView):
    queryset = Affiliate.affiliates.active()
    template_name = "affiliates/affiliate_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'eoy_data': self.object.current_data(),
            'org_type': 'Affiliate',
        })
        return context


class AffiliatePDFView(PDFMixin, AffiliateView):
    template_name = "affiliates/affiliate_pdf.html"


class AffiliateSearchView(SearchView):
    """
    List and search for affiliates
    """
    context_object_name = "affiliates"
    form_class = AffiliateSearchForm
    queryset = Affiliate.affiliates.active()
    template_name = "affiliates/affiliate_list.html"
