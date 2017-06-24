from django.conf.urls import url

from network_search.core import views

urlpatterns = [
    url(r'^$', view=views.HomePage.as_view(), name="home"),
]
