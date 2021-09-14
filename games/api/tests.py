import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()

@pytest.fixture(scope='module')
def setUp(self):

    new_user = User.objects.create_user(username='artemka', email='artem@gmail.com', password='weron1234')
    new_user.is_active = True
    new_user.save()

    body_data = {
        'email': 'artem@gmail.com',
        'password': 'weron1234'
    }
    response_from_login = self.client.post('http://127.0.0.1:8000/auth/login/', body_data,
                                format='json')

    self.token = response_from_login.data['access']
    self.rest_auth_login()


# def rest_auth_login(self):
#     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
#
#
# def test_getting_games(self):
#     response = self.client.get(reverse('game_list'), format='json')
#
#     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     self.assertIn('result', response)

