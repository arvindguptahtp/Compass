from easy_pdf.views import PDFTemplateResponseMixin
from django.views.generic import DetailView

from network_search.core.views import SearchView
from network_search.affiliates.forms import AffiliateSearchForm
from network_search.affiliates.models import Affiliate


class AffiliateView(DetailView):
    queryset = Affiliate.affiliates.active()
    template_name = "affiliates/affiliate_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'eoy_data': self.object.current_data(),
        })
        return context


class AffiliatePDFView(PDFTemplateResponseMixin, AffiliateView):
    template_name = "affiliates/affiliate_pdf.html"


class AffiliateSearchView(SearchView):
    """
    List and search for affiliates
    """
    context_object_name = "affiliates"
    form_class = AffiliateSearchForm
    queryset = Affiliate.affiliates.active()
    template_name = "affiliates/affiliate_list.html"
