from django.conf.urls.defaults import patterns
from django.conf.urls import url

import machines.views

urlpatterns = patterns('',
    url(r'^$', machines.views.all_machines),
    url(r'^/(?P<machine_name>[a-zA-Z]+)$', machines.views.detail, name='detail'),
)
