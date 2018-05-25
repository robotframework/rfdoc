from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

import rfdoc.settings as settings
from rfdoc.rfdocapp import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^upload/?$', views.upload, name='upload'),
    url(r'^search/?$', views.search, name='search'),
    url(r'^lib/([^/]*)$', views.library, name='library'),
    url(r'^lib/(.*)/(.*)$', views.library, name='version'),
    url(r'^$', views.index, name='root')
]

# Force Django to serve static assets, if this is not the production
if settings.PRODUCTION is False:
    urlpatterns.append(url(
        r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT
        })
    )
