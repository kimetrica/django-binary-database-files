import os

from django.conf import settings

def write_file(name, content, overwrite=False):
    """
    Writes the given content to the relative filename under the MEDIA_ROOT.
    """
    fqfn = os.path.join(settings.MEDIA_ROOT, name)
    fqfn = os.path.normpath(fqfn)
    if os.path.isfile(fqfn) and not overwrite:
        return
    dirs,fn = os.path.split(fqfn)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    open(fqfn, 'wb').write(content)
