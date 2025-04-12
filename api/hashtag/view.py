from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from ..post.serializer import *
from rest_framework.permissions import IsAuthenticated

class CreateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, hashtag_name):
        hashtag_name = hashtag_name.lower()
        serializer = HashtagCreateRequestSerializer(data={
            "name": hashtag_name
        })
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=201)
        else:
            return Response(serializer.errors, status=400)
        
class SearchView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, hashtag_name):
        hashtag_name = hashtag_name.lower()
        hashtags = Hashtag.objects.filter(name__icontains=hashtag_name)
        
        serializer = HashtagResponseSerializer(hashtags, many=True)
        return Response({"hashtags": serializer.data}, status=200)
    
class PostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, hashtag_name):
        hashtag_name = hashtag_name.lower()
        hashtags = Hashtag.objects.filter(name=hashtag_name)
        if not hashtags.exists():
            return Response({"error": "Hashtag not found."}, status=404)
        
        hashtag = hashtags.first()
        posts = hashtag.posts.all()
        
        serializer = PostViewResponseSerializer(posts, many=True)
        return Response(serializer.data, status=200)

class PictureView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, hashtag_name):
        hashtag_name = hashtag_name.lower()
        hashtags = Hashtag.objects.filter(name=hashtag_name)
        if not hashtags.exists():
            return Response({"error": "Hashtag not found."}, status=404)
        
        hashtag = hashtags.first()
        posts = hashtag.posts.all()
        
        pictures = []
        for post in posts:
            pictures.extend(post.pictures.all())
        
        serializer = PictureViewResponseSerializer(pictures, many=True)
        return Response({"pictures": serializer.data}, status=200)