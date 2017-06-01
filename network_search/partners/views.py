from django.views.generic import DetailView
from network_search.partners.models import Partner


class PartnerView(DetailView):
    queryset = Partner.partners.active()


