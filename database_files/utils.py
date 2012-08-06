#from grp import getgrnam
#from pwd import getpwnam
import os
import hashlib

from django.conf import settings

def is_fresh(name, content_hash):
    """
    Returns true if the file exists on the local filesystem and matches the
    content in the database. Returns false otherwise.
    """
    if not content_hash:
        return False
    fqfn = os.path.join(settings.MEDIA_ROOT, name)
    fqfn = os.path.normpath(fqfn)
    if not os.path.isfile(fqfn):
        return False
    local_content_hash = get_file_hash(fqfn)
    return local_content_hash == content_hash

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

def get_file_hash(fin):
    """
    Iteratively builds a file hash without loading the entire file into memory.
    """
    if isinstance(fin, basestring):
        fin = open(fin)
    h = hashlib.sha512()
    for text in fin.readlines():
        if not isinstance(text, unicode):
            text = unicode(text, encoding='utf-8', errors='replace')
        h.update(text.encode('utf-8', 'replace'))
    return h.hexdigest()

def get_text_hash(text):
    """
    Returns the hash of the given text.
    """
    h = hashlib.sha512()
    if not isinstance(text, unicode):
        text = unicode(text, encoding='utf-8', errors='replace')
    h.update(text.encode('utf-8', 'replace'))
    return h.hexdigest()

get_text_hash_0004 = get_text_hash
