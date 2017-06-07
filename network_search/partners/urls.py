from django.conf.urls import url

from network_search.partners.views import PartnerView
from network_search.partners.views import PartnerSearchView

urlpatterns = [
    url(r'^$', view=PartnerSearchView.as_view(), name="partner_list"),
    url(r'^(?P<pk>\d+)/$', view=PartnerView.as_view(), name="partner_detail"),
]
