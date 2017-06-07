from django.conf.urls import url

from network_search.affiliates.views import AffiliateView, AffiliateSearchView

urlpatterns = [
    url(r'^$', view=AffiliateSearchView.as_view(), name="affiliate_list"),
    url(r'^(?P<pk>\d+)/$', view=AffiliateView.as_view(), name="affiliate_detail"),
]
