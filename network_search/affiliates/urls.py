from django.conf.urls import url

from network_search.affiliates import views

urlpatterns = [
    url(r'^$', view=views.AffiliateSearchView.as_view(), name="affiliate_list"),
    url(r'^(?P<pk>\d+)/$', view=views.AffiliateView.as_view(), name="affiliate_detail"),
    url(r'^(?P<pk>\d+)\.pdf$', view=views.AffiliatePDFView.as_view(), name="affiliate_pdf"),
]
