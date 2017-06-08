from django.conf.urls import url

from network_search.programs import views

urlpatterns = [
    url(r'^$', view=views.ProgramSearchView.as_view(), name="program_list"),
    url(r'^(?P<pk>\d+)/$', view=views.ProgramView.as_view(), name="program_detail"),
    url(r'^(?P<pk>\d+)\.pdf$', view=views.ProgramPDFView.as_view(), name="program_pdf"),
]
