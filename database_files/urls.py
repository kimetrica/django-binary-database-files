try:
    from django.urls import re_path
except ImportError:
    # Django 1.11
    from django.conf.urls import url as re_path
from database_files import views

urlpatterns = [
    re_path(r'^files/(?P<name>.+)$',
        views.serve_mixed,
        name='database_file'),
]
