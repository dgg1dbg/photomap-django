from django.db import models
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File
import uuid

class PictureManager(models.Manager):
    def create_picture(self, file, longitude, latitude, description, post):
        extension = os.path.splitext(file.name)[1]
        unique_filename = f"{uuid.uuid4().hex}{extension}"

        folder_path = os.path.join(settings.MEDIA_ROOT, 'pictures')
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, unique_filename)
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        file_dir = os.path.join('pictures', unique_filename)
        return self.create(fileDir=file_dir, longitude=longitude, latitude=latitude, description=description, post=post)

    def delete_picture(self, picture):
        file_path = os.path.join(settings.MEDIA_ROOT, picture.fileDir)
        if os.path.exists(file_path):
            os.remove(file_path)
        picture.delete()

class Picture(models.Model):
    objects = PictureManager()
    fileDir = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    description = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='pictures')