from .view import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('/view/<int:picture_id>', ViewView.as_view(), name='view_picture'),
    path('/viewAll', ViewView.as_view(), name='view_pictures'),
    path('', FileView.as_view(), name='file_picture'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)