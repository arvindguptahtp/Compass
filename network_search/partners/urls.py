from django.conf.urls import url

from network_search.partners.views import PartnerView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', view=PartnerView.as_view(), name="partner_detail"),
]
