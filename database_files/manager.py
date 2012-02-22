from django.db import models
import os

class FileManager(models.Manager):
    def get_from_name(self, name):
#        print 'name:',name
#        return self.get(pk=os.path.splitext(os.path.split(name)[1])[0])
        return self.get(name=name)