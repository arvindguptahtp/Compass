from django.views.generic import DetailView

from easy_pdf.views import PDFTemplateResponseMixin
from network_search.core.views import SearchView
from network_search.affiliates.forms import AffiliateSearchForm
from network_search.affiliates.models import Affiliate


class AffiliateView(DetailView):
    queryset = Affiliate.affiliates.active()
    template_name = "affiliates/affiliate_detail.html"


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
