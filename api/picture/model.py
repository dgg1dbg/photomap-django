from django.db import models
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File
import uuid
import redis
from ..tasks.picture import compress_and_upload_image, delete_picture

r = redis.StrictRedis(host='redis', port=6379, db=2)

class PictureManager(models.Manager):
    def create_picture(self, file, longitude, latitude, description, post):
        file_id = str(uuid.uuid4())
        file_bytes = file.read()
        r.set(file_id, file_bytes)

        for size in ['small', 'medium', 'large']:
            compress_and_upload_image.delay(file_id, size)

        return self.create(file_id=file_id, longitude=longitude, latitude=latitude, description=description, post=post)

    def delete_picture(self, picture):
        delete_picture.delay(picture.file_id)
        picture.delete()

    def get_by_url(self, url):
        filename = url.split('/')[-1]
        base = filename.rsplit('.', 1)[0]
        file_id = base.rsplit('_', 1)[0]
        return self.get(file_id=file_id)

class Picture(models.Model):
    objects = PictureManager()
    file_id = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    description = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='pictures')