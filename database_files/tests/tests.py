import os
import StringIO

from django.core import files
from django.test import TestCase
from django.core.files.storage import default_storage

from database_files.models import File
from database_files.tests.models import Thing

DIR = os.path.abspath(os.path.split(__file__)[0])

class DatabaseFilesTestCase(TestCase):
    def test_adding_file(self):
        
        # Create default thing storing reference to file
        # in the local media directory.
        fqfn = os.path.join(DIR,'media/i/special/test.txt')
        open(fqfn,'w').write('hello there')
        o = Thing()
        o.upload = 'i/special/test.txt'
        o.save()
        id = o.id
        
        # Confirm thing was saved.
        Thing.objects.update()
        q = Thing.objects.all()
        self.assertEqual(q.count(), 1)
        self.assertEqual(q[0].upload.name, 'i/special/test.txt')
        
        # Confirm the file only exists on the file system
        # and hasn't been loaded into the database.
        q = File.objects.all()
        self.assertEqual(q.count(), 0)
        
        # Verify we can read the contents of thing.
        o = Thing.objects.get(id=id)
        self.assertEqual(o.upload.read(), "hello there")
        
        # Verify that by attempting to read the file, we've automatically
        # loaded it into the database.
        File.objects.update()
        q = File.objects.all()
        self.assertEqual(q.count(), 1)
        self.assertEqual(q[0].content, "hello there")
        
        # Load a dynamically created file outside /media.
        test_file = files.temp.NamedTemporaryFile(
            suffix='.txt',
            dir=files.temp.gettempdir()
        )
        test_file.write('1234567890')
        test_file.seek(0)
        t = Thing.objects.create(
            upload=files.File(test_file),
        )
        self.assertEqual(File.objects.count(), 2)
        t = Thing.objects.get(pk=t.pk)
        self.assertEqual(t.upload.file.size, 10)
        self.assertEqual(t.upload.file.name[-4:], '.txt')
        self.assertEqual(t.upload.file.read(), '1234567890')
        t.upload.delete()
        self.assertEqual(File.objects.count(), 1)
        
        # Confirm when delete a file from the database, we also delete it from
        # the filesystem.
        self.assertEqual(default_storage.exists('i/special/test.txt'), True)
        default_storage.delete('i/special/test.txt')
        self.assertEqual(default_storage.exists('i/special/test.txt'), False)
        self.assertEqual(os.path.isfile(fqfn), False)

class DatabaseFilesViewTestCase(TestCase):
    fixtures = ['test_data.json']
    
    def test_reading_file(self):
        self.assertEqual(File.objects.count(), 1)
        response = self.client.get('/files/1.txt')
        self.assertEqual(response.content, '1234567890')
        self.assertEqual(response['content-type'], 'text/plain')
        self.assertEqual(unicode(response['content-length']), '10')
