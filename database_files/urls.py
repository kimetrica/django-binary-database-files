from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^files/(?P<name>.+)$', 'database_files.views.serve', name='database_file'),
)
