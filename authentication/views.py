import logging

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_auth.models import TokenModel
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
            new_user_token = TokenModel.objects.create(user=new_user)
            send_activation_mail(request, new_user, new_user_token.key)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate_account(request, token):
    user = get_object_or_404(TokenModel, key=token)
    if user:
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. You already logged in!')

    return HttpResponse('Activation link is invalid!')


class Logout(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
