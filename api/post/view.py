from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from ..picture.model import Picture
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

def parse_coordinates(coordinates):
    parsed_coordinates = [list(map(float, coord[1:-1].split(','))) for coord in coordinates]
    return parsed_coordinates

class CreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        descriptions = request.data.getlist('descriptions')
        files = request.FILES.getlist('files')
        coordinates = parse_coordinates(request.data.getlist('coordinates'))
        picture_list = []
        if len(files) != len(descriptions) or len(files) != len(coordinates):
            return Response({"error": "The number of files and descriptions must be the same."}, status=400)
        for i in range(len(files)):
            picture_list.append({
                "description": descriptions[i],
                "file": files[i],
                "longitude": coordinates[i][0],
                "latitude": coordinates[i][1]
            })
        serializer = PostCreateRequestSerializer(data={
            "name": request.data.get('name'),
            "date": request.data.get('date'),
            "time": request.data.get('time'),
            "description": request.data.get('description'),
            "pictures": picture_list,
            "hashtags": request.data.get('hashtag')
        },
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            post = serializer.instance
            response_serializer = PostCreateResponseSerializer(post)
            return Response(response_serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
class EditView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, post_id):
        requested_user = request.user
        post = Post.objects.get(id=post_id)
        if post.user != requested_user:
            return Response({"error": "You do not have permission to edit this post."}, status=403)
        if not post:
            return Response({"error": "Post not found."}, status=404)
        descriptions = request.data.getlist('descriptions')
        files = request.FILES.getlist('files')
        paths = request.data.getlist('paths')
        fileandpaths = paths + files
        coordinates = parse_coordinates(request.data.getlist('coordinates'))
        picture_list = []
        if len(fileandpaths) != len(descriptions) or len(fileandpaths) != len(coordinates):
            return Response({"error": "The number of files and descriptions must be the same."}, status=400)
        for i in range(len(fileandpaths)):
            picture_list.append({
                "description": descriptions[i],
                "file": fileandpaths[i],
                "longitude": coordinates[i][0],
                "latitude": coordinates[i][1]
            })
        serializer = PostEditRequestSerializer(instance=post, data={
            "name": request.data.get('name'),
            "date": request.data.get('date'),
            "time": request.data.get('time'),
            "description": request.data.get('description'),
            "pictures": picture_list,
            "hashtags": request.data.get('hashtag')
        },
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            post = serializer.instance
            response_serializer = PostCreateResponseSerializer(post)
            return Response(response_serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
        
class ViewView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostViewResponseSerializer(post)
        return Response(serializer.data, status=200)
    
