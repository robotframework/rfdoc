import os.path

from django.conf.urls.defaults import *

from rfdoc.rfdocapp import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^upload/?$', views.upload),
    (r'^search/?$', views.search),
    (r'^lib/(.*)', views.library),
    (r'^$', views.index),
)
