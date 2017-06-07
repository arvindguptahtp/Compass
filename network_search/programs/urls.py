from django.conf.urls import url

from network_search.programs.views import ProgramView
from network_search.programs.views import ProgramSearchView

urlpatterns = [
    url(r'^$', view=ProgramSearchView.as_view(), name="program_list"),
    url(r'^(?P<pk>\d+)/$', view=ProgramView.as_view(), name="program_detail"),
]
