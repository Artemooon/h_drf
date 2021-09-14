import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..tasks import send_activation_mail, send_weekly_reminder_confirm_email

User = get_user_model()


@pytest.mark.django_db
class CeleryTasksTest(APITestCase):
    def setUp(self) -> None:
        new_user = User.objects.create_user(username='artemka', email='artem@gmail.com', password='weron1234')

        self.new_user = new_user

    def test_send_activation_mail_task(self):
        task = send_activation_mail.s('http://127.0.0.1/', self.new_user.id,
                                      'auth/account-activate/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMxMTMyODg5LCJqdGkiOiJkZGIyODVmZmE0NTc0YjkxYjYzODRkNjU2YTRmZjlkNSIsInVzZXJfaWQiOjMxfQ.42Qs3oSrWuAK4dmqM3ZV5LHPPJf8AjKe_6HGVoBnzlM/').apply()

        assert task.status == 'SUCCESS'
        assert task.result is None

    def test_send_reminder_email_task(self):
        task = send_weekly_reminder_confirm_email.s().apply()

        assert task.status == 'SUCCESS'
        assert task.result is None
