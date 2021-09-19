from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .mails import generate_mail_confirmation_url_token
from ..tasks import send_activation_mail

User = get_user_model()


def register_new_user(serializer_data):
    new_user = User.objects.get(id=serializer_data['id'])
    confirm_url_token = generate_mail_confirmation_url_token(new_user)

    current_site = Site.objects.get_current()
    current_domain = current_site.domain

    send_activation_mail.delay(current_domain, new_user.id, confirm_url_token)
    registered_user_dict = {'user': serializer_data}

    return registered_user_dict


def activate_user_account(decoded_token):
    user = User.objects.filter(id=decoded_token['user_id'])
    if user.exists():
        user = user.first()
        user.is_active = True
        user.is_reminder_notified = True
        user.save()
        return Response({'message': 'Thank you for your email confirmation!'}, status=status.HTTP_200_OK)

    return Response({'message': 'Activation link is invalid!'}, status=status.HTTP_200_OK)


def move_refresh_token_to_blacklist(refresh_token):
    token = RefreshToken(refresh_token)
    token.blacklist()
