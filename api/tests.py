from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_auth.models import TokenModel
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="artemka", password="dodik123")
        self.token = TokenModel.objects.create(user=self.user)
        self.rest_auth_login()

    def rest_auth_login(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token.key))

    def test_register(self):
        body_data = {
            'username': 'artem12',
            'email': 'artema@gamil1.com',
            'password': 'dodik1234',
            'confirm_password': 'dodik1234'
        }
        response = self.client.post('http://127.0.0.1:8000/auth/register/', body_data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=response.data['id']).id, response.data['id'])

    def test_login(self):
        body_data = {
            'username': 'artemka',
            'password': 'dodik123'
        }

        response = self.client.post('http://127.0.0.1:8000/rest-auth/login/', body_data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['key'], TokenModel.objects.get(key=response.data['key']).key)

    def test_getting_games(self):
        response = self.client.get(reverse('game_list'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

