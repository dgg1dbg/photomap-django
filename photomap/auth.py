from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from rest_framework.authentication import BaseAuthentication


class LoggingJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            print("No token found in request headers")
            return None
        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        return (user, validated_token)
    
class NoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return None