from .view import *
from django.urls import path

urlpatterns = [
    path('post/<str:hashtag_name>', PostView.as_view(), name='view_post'),
    path('picture/<str:hashtag_name>', PictureView.as_view(), name='view_picture'),
    path('create/<str:hashtag_name>', CreateView.as_view(), name='create_hashtag'),
    path('search/<str:hashtag_name>', SearchView.as_view(), name='search_hashtag'),
]
