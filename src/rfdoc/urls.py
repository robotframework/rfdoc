from django.conf.urls import *

from rfdoc.rfdocapp import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^upload/?$', views.upload),
    (r'^search/?$', views.search),
    (r'^lib/(.*)', views.library),
    (r'^$', views.index),
)
