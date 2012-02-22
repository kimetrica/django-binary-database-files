import base64

from django.db import models

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
        blank=False,
        null=False)

    _content = models.TextField(db_column='content')
    
    @property
    def content(self):
        return base64.b64decode(self._content)
    
    @content.setter
    def content(self, v):
        self._content = base64.b64encode(v)
        