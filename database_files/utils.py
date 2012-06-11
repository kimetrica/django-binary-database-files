#from grp import getgrnam
#from pwd import getpwnam
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
    
    # Set ownership and permissions.
    uname = getattr(settings, 'DATABASE_FILES_USER', None)
    gname = getattr(settings, 'DATABASE_FILES_GROUP', None)
    if gname:
        gname = ':'+gname
    if uname:
        os.system('chown -RL %s%s "%s"' % (uname, gname, dirs))

    # Set permissions.
    perms = getattr(settings, 'DATABASE_FILES_PERMS', None)
    if perms:
        os.system('chmod -R %s "%s"' % (perms, dirs))