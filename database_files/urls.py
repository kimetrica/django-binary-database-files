
try:
    # Removed in Django 1.6
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url

urlpatterns = patterns('',
#    url(r'^files/(?P<name>.+)$',
#        'database_files.views.serve',
#        name='database_file'),
    url(r'^files/(?P<name>.+)$',
        'database_files.views.serve_mixed',
        name='database_file'),
)
