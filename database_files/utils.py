#from grp import getgrnam
#from pwd import getpwnam
import os
import hashlib

import six

from django.conf import settings

def is_fresh(name, content_hash):
    """
    Returns true if the file exists on the local filesystem and matches the
    content in the database. Returns false otherwise.
    """
    if not content_hash:
        return False
    
    # Check that the actual file exists.
    fqfn = os.path.join(settings.MEDIA_ROOT, name)
    fqfn = os.path.normpath(fqfn)
    if not os.path.isfile(fqfn):
        return False
    
    # Check for cached hash file.
    hash_fn = get_hash_fn(name)
    if os.path.isfile(hash_fn):
        return open(hash_fn).read().strip() == content_hash
    
    # Otherwise, calculate the hash of the local file.
    fqfn = os.path.join(settings.MEDIA_ROOT, name)
    fqfn = os.path.normpath(fqfn)
    if not os.path.isfile(fqfn):
        return False
    local_content_hash = get_file_hash(fqfn)
    return local_content_hash == content_hash

def get_hash_fn(name):
    """
    Returns the filename for the hash file.
    """
    fqfn = os.path.join(settings.MEDIA_ROOT, name)
    fqfn = os.path.normpath(fqfn)
    dirs,fn = os.path.split(fqfn)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    fqfn_parts = os.path.split(fqfn)
    hash_fn = os.path.join(fqfn_parts[0],
        settings.DB_FILES_DEFAULT_HASH_FN_TEMPLATE % fqfn_parts[1])
    return hash_fn

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
    
    # Cache hash.
    hash = get_file_hash(fqfn)
    hash_fn = get_hash_fn(name)
    try:
        # Write out bytes in Python3.
        value = six.binary_type(hash, 'utf-8')
    except TypeError:
        value = hash
    open(hash_fn, 'wb').write(value)
    
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

def get_file_hash(fin,
    force_encoding=settings.DB_FILES_DEFAULT_ENFORCE_ENCODING,
    encoding=settings.DB_FILES_DEFAULT_ENCODING,
    errors=settings.DB_FILES_DEFAULT_ERROR_METHOD,
    chunk_size=128):
    """
    Iteratively builds a file hash without loading the entire file into memory.
    """
    if isinstance(fin, six.string_types):
        fin = open(fin, 'rb')
    h = hashlib.sha512()
    while 1:
        text = fin.read(chunk_size)
        if not text:
            break
        if force_encoding:
            if not isinstance(text, six.text_type):
                text = six.text_type(text, encoding=encoding, errors=errors)
            h.update(text.encode(encoding, errors))
        else:
            h.update(text)
    return h.hexdigest()

def get_text_hash_0004(text):
    """
    Returns the hash of the given text.
    """
    h = hashlib.sha512()
    if not isinstance(text, six.text_type):
        text = six.text_type(text, encoding='utf-8', errors='replace')
    h.update(text.encode('utf-8', 'replace'))
    return h.hexdigest()

def get_text_hash(text,
    force_encoding=settings.DB_FILES_DEFAULT_ENFORCE_ENCODING,
    encoding=settings.DB_FILES_DEFAULT_ENCODING,
    errors=settings.DB_FILES_DEFAULT_ERROR_METHOD):
    """
    Returns the hash of the given text.
    """
    h = hashlib.sha512()
    if force_encoding:
        if not isinstance(text, six.text_type):
            text = six.text_type(text, encoding=encoding, errors=errors)
        h.update(text.encode(encoding, errors))
    else:
        h.update(text)
    return h.hexdigest()
