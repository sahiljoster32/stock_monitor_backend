"""
Module for defining views of users app. It can be
function based or class based.
"""

from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, permissions, authentication
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterUserAPIView(generics.CreateAPIView):
    """
    API view for registering a new user.

    Attributes:
        permission_classes: Specifies the permission for users, currently
            `AllowAny` is used which allows any user to access this view.
        serializer_class: The serializer class used for validating and
            deserializing the request data.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(ObtainAuthToken):
    """
    API view for logging an existing user.

    Attributes:
        permission_classes: Specifies the permission for users, currently
            `AllowAny` is used which allows any user to access this view.
        serializer_class: The serializer class used for validating and
            deserializing the request data.
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



    def post(self, request, *args, **kwargs):
        """Handles the POST request for logging int the user. Also, validates
        the provided credentials, generates a token for the authenticated user,
        and returns a response containing the token along with additional
        user information.

        Args:
            request (Request): A Django request object.
            *args: Additional named arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Response object containing the token and user information.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response = {
            'token': token.key,
            "user_email": user.email,
            "user_name": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "watch_list_symbols": user.watchlist.symbols
        }
        return Response(response)
