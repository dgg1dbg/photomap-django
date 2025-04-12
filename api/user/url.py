from django.urls import path
from .view import *

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('signin', SigninView.as_view(), name='signin'),
    path('delete', DeleteView.as_view(), name='delete'),
    path('edit', EditView.as_view(), name='edit'),
    path('view', ViewView.as_view(), name='view'),
    path('view/<str:username>', DetailView.as_view(), name='view-detail'),
]