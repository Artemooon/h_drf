from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse


def send_activation_mail(request, user, new_user_token):
    current_domain = get_current_site(request).domain
    mail_subject = 'Activation code from Game API'
    user_token = new_user_token
    confirm_url = reverse('activate_account', args=[user_token])
    mail_body = f"Hi {user.username},\nPlease click on the link to confirm your registration,\nhttp://{current_domain}" \
                f"{confirm_url}\n\nIf you think, it's not you, then just ignore this email."
    email = EmailMessage(mail_subject, mail_body, to=[user.email])
    email.send()
