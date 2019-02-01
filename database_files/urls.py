from django.urls import url
from database_files import views

urlpatterns = [
    url(r'^files/(?P<name>.+)$',
        views.serve_mixed,
        name='database_file'),
]
