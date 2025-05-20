from django.db import models
from ..user.model import User
from ..picture.model import Picture


class Post(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    hashtags = models.ManyToManyField('Hashtag', related_name='posts')
    place = models.CharField(max_length=100)

    def delete(self, *args, **kwargs):
        for picture in self.pictures.all():
            Picture.objects.delete_picture(picture)
        super().delete(*args, **kwargs)