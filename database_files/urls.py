from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^files/(?P<name>.+)$', 'database_files.views.serve', name='database_file'),
)
