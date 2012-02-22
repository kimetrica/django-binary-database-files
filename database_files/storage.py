import os
import StringIO

from django.conf import settings
from django.core import files
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse

from database_files import models

class DatabaseStorage(FileSystemStorage):
    
    def _generate_name(self, name, pk):
        """
        Replaces the filename with the specified pk and removes any dir
        """
        #dir_name, file_name = os.path.split(name)
        #file_root, file_ext = os.path.splitext(file_name)
        #return '%s%s' % (pk, file_name)
        return name
    
    def _open(self, name, mode='rb'):
        """
        Open file with filename `name` from the database.
        """
        try:
            # Load file from database.
            f = models.File.objects.get_from_name(name)
            content = f.content
            size = f.size
        except models.File.DoesNotExist:
            # If not yet in the database, check the local file system
            # and load it into the database if present.
            fqfn = self.path(name)
            if os.path.isfile(fqfn):
                self._save(name, open(fqfn, mode))
                fh = super(DatabaseStorage, self)._open(name, mode)
                content = fh.read()
                size = fh.size
            else:
                # Otherwise we don't know where the file is.
                return
        # Normalize the content to a new file object.
        fh = StringIO.StringIO(content)
        fh.name = name
        fh.mode = mode
        fh.size = size
        o = files.File(fh)
        return o
    
    def _save(self, name, content):
        """
        Save file with filename `name` and given content to the database.
        """
        full_path = self.path(name)
        try:
            size = content.size
        except AttributeError:
            size = os.path.getsize(full_path)
        f = models.File.objects.create(
            content=content.read(),
            size=size,
            name=name,
        )
        return self._generate_name(name, f.pk)
    
    def exists(self, name):
        """
        Returns true if a file with the given filename exists in the database.
        Returns false otherwise.
        """
        if models.File.objects.filter(name=name).count() > 0:
            return True
        return super(DatabaseStorage, self).exists(name)
    
    def delete(self, name):
        """
        Deletes the file with filename `name` from the database and filesystem.
        """
        full_path = self.path(name)
        try:
            models.File.objects.get_from_name(name).delete()
        except models.File.DoesNotExist:
            pass
        return super(DatabaseStorage, self).delete(name)
    
    def url(self, name):
        """
        Returns the web-accessible URL for the file with filename `name`.
        """
        return os.path.join(settings.MEDIA_URL, name)
        #return reverse('database_file', kwargs={'name': name})
    
    def size(self, name):
        """
        Returns the size of the file with filename `name` in bytes.
        """
        full_path = self.path(name)
        try:
            return models.File.objects.get_from_name(name).size
        except models.File.DoesNotExist:
            return super(DatabaseStorage, self).size(name)
