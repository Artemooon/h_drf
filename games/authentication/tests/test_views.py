import jwt
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


@pytest.mark.django_db
class AuthenticationTest(APITestCase):

    def setUp(self) -> None:
        new_user = User.objects.create_user(username='artema', email='artem@gmail.com', password='weron1234')
        new_user.is_active = True
        new_user.save()

    def authorize_user(self):
        url = reverse('token_obtain_pair')
        body = {
            "email": "artem@gmail.com",
            "password": "weron1234"
        }
        response = self.client.post(url, body, format='json')

        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def register_user(self):
        url = reverse('user_register')
        body_data = {
            "username": "artemka1",
            "email": "artem.logachov772@gmail.com",
            "password": "weron123",
            "confirm_password": "weron123"
        }
        self.client.post(url, body_data, format='json')


    def test_register_new_user(self):
        body_data = {
            "username": "artemka",
            "email": "artem.logachov773@gmail.com",
            "password": "weron123",
            "confirm_password": "weron123"
        }
        response = self.client.post(reverse('user_register'), body_data,
                                    format='json')

        assert response.status_code == status.HTTP_200_OK
        assert User.objects.get(id=response.data['user']['id']).username == response.data['user']['username']

    def test_register_with_password_confirm_errors(self):
        body_data = {
            "username": "artemka",
            "email": "artem.logachov773@gmail.com",
            "password": "weron123",
            "confirm_password": "weron12"
        }
        response = self.client.post(reverse('user_register'), body_data,
                                    format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'][0] == 'Those passwords don\'t match.'

    def test_register_with_email_already_exists(self):
        body_data = {
            "username": "artemka",
            "email": "artem@gmail.com",
            "password": "weron123",
            "confirm_password": "weron123"
        }
        response = self.client.post(reverse('user_register'), body_data,
                                    format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'][0] == 'user with this email already exists.'

    def test_register_with_username_already_exists(self):
        body_data = {
            "username": "artema",
            "email": "artem.logachov773@gmail.com",
            "password": "weron123",
            "confirm_password": "weron123"
        }
        response = self.client.post(reverse('user_register'), body_data,
                                    format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'][0] == 'user with this username already exists.'

    def test_logout_user_refresh_error(self):
        self.authorize_user()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        url = reverse('user_logout')
        body = {
            "refresh": 'fsdfsdfsdfsdf',
        }
        response = self.client.post(url, body, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_user(self):
        self.authorize_user()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        url = reverse('user_logout')
        body = {
            "refresh": self.refresh_token,
        }
        response = self.client.post(url, body, format='json')

        assert response.status_code == status.HTTP_200_OK

    def test_login_user(self):
        url = reverse('token_obtain_pair')
        body = {
            "email": "artem@gmail.com",
            "password": "weron1234"
        }
        response = self.client.post(url, body, format='json')
        decoded_access = jwt.decode(response.data['access'], settings.SECRET_KEY, algorithms=["HS256"])
        decoded_refresh = jwt.decode(response.data['refresh'], settings.SECRET_KEY, algorithms=["HS256"])

        assert response.status_code == status.HTTP_200_OK
        assert decoded_access['user_id'] == decoded_refresh['user_id']
        assert decoded_access['token_type'] == 'access'
        assert decoded_refresh['token_type'] == 'refresh'

    def test_login_user_password_error(self):
        url = reverse('token_obtain_pair')
        body = {
            "email": "artem@gmail.com",
            "password": ""
        }
        response = self.client.post(url, body, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'][0] == 'This field may not be blank.'

    def test_login_user_credentials_error(self):
        url = reverse('token_obtain_pair')
        body = {
            "email": "artem12@gmail.com",
            "password": "weron12"
        }
        response = self.client.post(url, body, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == 'No active account found with the given credentials'

    def test_refresh_access_token_with_bad_request(self):
        self.authorize_user()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('token_refresh')
        body = {
            "refresh": ""
        }
        response = self.client.post(url, body, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_refresh_access_token_with_bad_refresh_token(self):
        self.authorize_user()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('token_refresh')
        body = {
            "refresh": "daslkdasipdkiasjda"
        }
        response = self.client.post(url, body, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_access_token_success(self):
        self.authorize_user()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('token_refresh')
        body = {
            "refresh": self.refresh_token
        }
        response = self.client.post(url, body, format='json')

        assert response.status_code == status.HTTP_200_OK

