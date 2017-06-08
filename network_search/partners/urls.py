from django.conf.urls import url

from network_search.partners import views

urlpatterns = [
    url(r'^$', view=views.PartnerSearchView.as_view(), name="partner_list"),
    url(r'^(?P<pk>\d+)/$', view=views.PartnerView.as_view(), name="partner_detail"),
    url(r'^(?P<pk>\d+)\.pdf$', view=views.PartnerPDFView.as_view(), name="partner_pdf"),
]
