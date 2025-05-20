from django.urls import path
from .view import *

urlpatterns = [
    path('search', PlaceView.as_view(), name='search'),
]