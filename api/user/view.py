from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from photomap.auth import NoAuthentication

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return 'Bearer ' + str(refresh.access_token)




class SignupView(APIView):
    authentication_classes = [NoAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            response = Response({
                "message": "User created successfully",
            }, status=201)
            response['Authentication'] = token
            return response
        return Response(serializer.errors, status=400)
    
class SigninView(APIView):
    authentication_classes = [NoAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSigninRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    token = get_tokens_for_user(user)
                    response = Response({
                        "message": "User signed in successfully",
                        "token": token,
                    }, status=200)
                    return response
                else:
                    return Response({"error": "Invalid password"}, status=400)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        return Response(serializer.errors, status=400)
    
class EditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserEditRequestSerializer(request.user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User updated successfully",
            }, status=200)
        return Response(serializer.errors, status=400)
    
class ViewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserViewResponseSerializer(request.user)
        return Response(serializer.data, status=200)
    
class DetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserDetailViewResponseSerializer(user)
            return Response(serializer.data, status=200)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class DeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            user = request.user
            user.delete()
            return Response({"message": "User deleted successfully"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
