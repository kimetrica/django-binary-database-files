
from django.urls import re_path

from database_files import views


urlpatterns = [
#    url(r'^files/(?P<name>.+)$',
#        'database_files.views.serve',
#        name='database_file'),
    re_path(r'^files/(?P<name>.+)$',
        views.serve_mixed,
        name='database_file'),
]
