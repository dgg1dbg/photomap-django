from django.urls import path
from .view import *

urlpatterns = [
    path('create', CreateView.as_view(), name='create_post'),
    path('edit/<int:post_id>', EditView.as_view(), name='edit_post'),
    path('view/<int:post_id>', ViewView.as_view(), name='view_post'),
]