import base64
import os

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control

import mimetypes

from database_files.models import File

@cache_control(max_age=86400)
def serve(request, name):
    f = get_object_or_404(File, name=name)
    mimetype = mimetypes.guess_type(name)[0] or 'application/octet-stream'
    response = HttpResponse(f.content, mimetype=mimetype)
    response['Content-Length'] = f.size
    return response
