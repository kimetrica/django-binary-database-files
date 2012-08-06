import base64

from django.db import models
from django.utils import timezone

from database_files import utils
from database_files.manager import FileManager

class File(models.Model):
    
    objects = FileManager()
    
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        db_index=True)
    
    size = models.PositiveIntegerField(
        db_index=True,
        blank=False,
        null=False)

    _content = models.TextField(db_column='content')
    
    created_datetime = models.DateTimeField(
        db_index=True,
        default=timezone.now,
        verbose_name="Created datetime")
    
    _content_hash = models.CharField(
        db_column='content_hash',
        db_index=True,
        max_length=128,
        blank=True, null=True)
    
    def save(self, *args, **kwargs):
        
        # Check for and clear old content hash.
        if self.id:
            old = File.objects.get(id=self.id)
            if old._content != self._content:
                self._content_hash = None
                
        # Recalculate new content hash.
        self.content_hash
        
        return super(File, self).save(*args, **kwargs)
    
    @property
    def content(self):
        return base64.b64decode(self._content)
    
    @content.setter
    def content(self, v):
        self._content = base64.b64encode(v)
        
    @property
    def content_hash(self):
        if not self._content_hash and self._content:
            self._content_hash = utils.get_text_hash(self.content)
        return self._content_hash
    