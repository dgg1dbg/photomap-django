from django.urls import path, include
from .user.view import *

urlpatterns = [
    path('user/', include('api.user.url')),
    path('post/', include('api.post.url')),
    path('picture', include('api.picture.url')),
    path('hashtag/', include('api.hashtag.url'))
]