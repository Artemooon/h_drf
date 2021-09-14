import logging

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from .exceptions import BaseView
from .serializers import UserRegisterSerializer
from .services.registration import register_new_user, activate_user_account, move_refresh_token_to_blacklist

User = get_user_model()

logger = logging.getLogger(__name__)


class RegisterUser(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            registered_user = register_new_user(serializer.data)

            return Response(registered_user, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccount(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, token):

        try:
            decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.DecodeError:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        return activate_user_account(decode_token)


class Logout(generics.GenericAPIView, BaseView,):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
        except KeyError:
            return Response({'message': 'Provide refresh_token'}, status=status.HTTP_408_REQUEST_TIMEOUT)
        try:
            move_refresh_token_to_blacklist(refresh_token)
        except jwt.exceptions.InvalidTokenError:
            return Response({'message': 'Refresh token expired or invalid'}, status=status.HTTP_408_REQUEST_TIMEOUT)

        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
