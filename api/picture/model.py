from django.db import models
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File
import uuid
import redis
from ..tasks.picture import compress_and_upload_image, delete_picture
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.core.cache import cache
from .cache import get_grid_key_from_point

r = redis.StrictRedis(host='redis', port=6379, db=2)

class PictureManager(models.Manager):
    def create_picture(self, file, longitude, latitude, description, post):
        file_id = str(uuid.uuid4())
        file_bytes = file.read()
        r.set(file_id, file_bytes)

        for size in ['small', 'medium', 'large']:
            compress_and_upload_image.delay(file_id, size)

        location = Point(longitude, latitude)
        grid_key = get_grid_key_from_point(location)
        cache.delete(grid_key)
        return self.create(file_id=file_id, location=location, description=description, post=post)

    def delete_picture(self, picture):
        grid_key = get_grid_key_from_point(picture.location)
        cache.delete(grid_key)
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
    location = gis_models.PointField(spatial_index=True)
    description = models.TextField(blank=True, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='pictures')