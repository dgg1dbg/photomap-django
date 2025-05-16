from rest_framework.views import APIView
from .model import Picture
from .serializer import *
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from photomap.auth import NoAuthentication
from django.conf import settings
import os
from django.core.cache import cache
from .cache import get_grid_keys, get_cached_grid_data

class ViewView(APIView):
    authentication_classes = [NoAuthentication]
    permission_classes = [AllowAny]
    def get(self, request, picture_id=None):
        if picture_id is not None:
            try:
                picture = Picture.objects.get(id=picture_id)
            except Picture.DoesNotExist:
                return Response({"error": "Picture not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = PictureViewResponseSerializer(picture)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            grid_keys = get_grid_keys(request)
            results = []
            for grid_key in grid_keys:
                results.extend(get_cached_grid_data(grid_key))
            return Response(results, status=status.HTTP_200_OK)
    
class FileView(APIView):
    authentication_classes = [NoAuthentication]
    permission_classes = [AllowAny]
    def get(self, request):
        file_path = request.GET.get('dir')
        if not file_path:
            return Response({"error": "No file path provided."}, status=400)
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        if not os.path.exists(full_file_path):
            return Response({"error": "File not found."}, status=404)
        response = FileResponse(open(full_file_path, 'rb'))
        return response
    
