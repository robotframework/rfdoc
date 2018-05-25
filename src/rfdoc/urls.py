from django.conf.urls import include, patterns, url
from django.contrib import admin

import settings
from rfdocapp import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^upload/?$', views.upload, name='upload'),
    url(r'^search/?$', views.search, name='search'),
    url(r'^lib/([^/]*)$', views.library, name='library'),
    url(r'^lib/(.*)/(.*)$', views.library, name='version'),
    url(r'^$', views.index, name='root')
)

# Force Django to serve static assets, if this is not the production
if settings.PRODUCTION is False:
    urlpatterns += patterns('', (
        r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT
        }
    ))
