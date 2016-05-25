from django.conf.urls.defaults import patterns
from django.conf.urls import url

import machines.views

urlpatterns = patterns('',
    url(r'^$', machines.views.all_machines, name="all"),
    url(r'^/(?P<machine_name>[a-z0-9\-\.]+)$', machines.views.detail, name='detail'),
)

