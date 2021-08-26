import logging

import jwt
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from .mails import send_activation_mail
from .serializers import UserRegisterSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class RegisterUser(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            new_user = User.objects.get(id=serializer.data['id'])
            new_user_token = RefreshToken.for_user(new_user).access_token
            send_activation_mail(request, new_user, new_user_token)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccount(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, token):

        try:
            decode_token = jwt.decode(token, settings.SECRET_KEY,  algorithms=["HS256"])
        except jwt.DecodeError:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=decode_token['user_id'])
            if user:
                user.is_active = True
                user.save()
                return Response({'Thank you for your email confirmation!'}, status=status.HTTP_200_OK)

            return Response({'Activation link is invalid!'}, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError:
            return Response({'Activation link expired'}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except jwt.exceptions.InvalidTokenError:
            return Response({'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
