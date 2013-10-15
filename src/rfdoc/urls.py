from django.conf.urls import include, patterns, url
from django.contrib import admin

from rfdoc.rfdocapp import views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^upload/?$', views.upload),
    (r'^search/?$', views.search),
    (r'^lib/(.*)', views.library),
    (r'^$', views.index),
)
