
try:
    # Removed in Django 1.6
    from django.conf.urls.defaults import url
except ImportError:
    from django.conf.urls import url
    
try:
    # Relocated in Django 1.6
    from django.conf.urls.defaults import pattern
except ImportError:
    # Completely removed in Django 1.10
    try:    
        from django.conf.urls import patterns
    except ImportError:
        patterns = None

import database_files.views

_patterns = [
#    url(r'^files/(?P<name>.+)$',
#        database_files.views.serve,
#        name='database_file'),
    url(r'^files/(?P<name>.+)$',
        database_files.views.serve_mixed,
        name='database_file'),
]

if patterns is None:
    urlpatterns = _patterns
else:
    urlpatterns = patterns('', *_patterns)
