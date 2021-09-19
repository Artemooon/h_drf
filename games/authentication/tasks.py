from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from games.celery import app as celery
from .services.mails import weekly_reminder_confirmation_email

User = get_user_model()


@celery.task
def send_activation_mail(current_domain, user_id, confirm_url):
    user = User.objects.get(id=user_id)
    mail_subject = 'Activation link from Game API'
    msg_html = render_to_string('authentication/activation-mail-template.html',
                                {'username': user.username, 'confirm_url': confirm_url,
                                 'current_domain': current_domain})
    email = EmailMessage(mail_subject, msg_html, to=[user.email])
    email.send()
    return email.to

@celery.task
def send_weekly_reminder_confirm_email():
    all_users = weekly_reminder_confirmation_email()
    if all_users:
        for user in all_users:
            user.send()
    return 'Successfully send'
