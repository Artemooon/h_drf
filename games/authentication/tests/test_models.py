import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestModels:

    def test_user_in_list(self):
        User.objects.create_user(username='john', email='lennon@thebeatles.com',
                                 password='johnpassword')
        assert User.objects.count() == 1