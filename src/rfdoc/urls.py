from django.conf.urls import include, patterns, url
from django.contrib import admin

from rfdoc import settings
from rfdoc.rfdocapp import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^upload/?$', views.upload),
    (r'^search/?$', views.search),
    (r'^lib/(.*)', views.library),
    (r'^$', views.index)
)

# Force Django to serve static assets, if this is not the production
if settings.PRODUCTION is False:
    urlpatterns += patterns('', (
        r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT
        }
    ))
