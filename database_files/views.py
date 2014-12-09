import base64
import os

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control
from django.views.static import serve as django_serve

import mimetypes

from database_files.models import File

@cache_control(max_age=86400)
def serve(request, name):
    """
    Retrieves the file from the database.
    """
    f = get_object_or_404(File, name=name)
    f.dump()
    mimetype = mimetypes.guess_type(name)[0] or 'application/octet-stream'
    response = HttpResponse(f.content, content_type=mimetype)
    response['Content-Length'] = f.size
    return response

def serve_mixed(request, *args, **kwargs):
    """
    First attempts to serve the file from the filesystem,
    then tries the database.
    """
    name = kwargs.get('name') or kwargs.get('path')
    document_root = kwargs.get('document_root')
    document_root = document_root or settings.MEDIA_ROOT
    try:
        # First attempt to serve from filesystem.
        return django_serve(request, name, document_root)
    except Http404:
        # Then try serving from database.
        return serve(request, name)
    