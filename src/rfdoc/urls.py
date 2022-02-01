from django.urls import include, re_path
from django.contrib import admin
from django.views.static import serve


import rfdoc.settings as settings

from rfdoc.rfdocapp import views

admin.autodiscover()

app_name = "rfdocapp"

urlpatterns = [
    re_path(r'^admin/', admin.site.urls, name='admin'),
    re_path(r'^upload/?$', views.upload, name='upload'),
    re_path(r'^search/?$', views.search, name='search'),
    re_path(r'^lib/([^/]*)$', views.library, name='library'),
    re_path(r'^lib/(.*)/(.*)$', views.library, name='version'),
    re_path(r'^$', views.index, name='root')
]

# Force Django to serve static assets, if this is not the production
if settings.PRODUCTION is False:
    urlpatterns.append(re_path(
        r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT
        })
    )
