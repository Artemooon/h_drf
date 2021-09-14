from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

User = get_user_model()


def generate_mail_confirmation_url_token(new_user):
    confirm_token = RefreshToken.for_user(new_user).access_token
    confirm_url_token = reverse('activate_account', args=[confirm_token])

    return confirm_url_token


def weekly_reminder_confirmation_email():
    all_users = User.objects.filter(is_reminder_notified=False).all()
    mail_subject = 'User activation code from Game API'
    current_site = Site.objects.get(id=1)
    current_domain = current_site.domain

    email = None

    for user in all_users:
        user.is_reminder_notified = True
        user.save()
        confirm_url_token = generate_mail_confirmation_url_token(user)
        msg_html = render_to_string('authentication/remind-activation-mail-template.html',
                                    {'username': user.username, 'confirm_url': confirm_url_token,
                                     'current_domain': current_domain})
        email = EmailMessage(mail_subject, msg_html, to=[user.email])

        yield email

