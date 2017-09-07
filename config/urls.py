from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

from network_search.core.views import csrf_exempt_password

admin.site.site_header = "CIS Search Tool"
admin.site.site_title = "CIS Search Tool"

urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'', include('network_search.core.urls')),
    url(r'^protect/$', view=csrf_exempt_password, name="simple_auth_password"),
    url(r'^partners/', include('network_search.partners.urls')),
    url(r'^programs/', include('network_search.programs.urls')),
    url(r'^affiliates/', include('network_search.affiliates.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if 's3direct' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^s3direct/', include('s3direct.urls')),
    ]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
