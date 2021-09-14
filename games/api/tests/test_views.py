import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Game, Creator, GameCategory

User = get_user_model()


@pytest.mark.django_db
class ApiCRUDTest(APITestCase):
    def setUp(self) -> None:
        new_user = User.objects.create_user(username='artemka', email='artem@gmail.com', password='weron1234')
        new_user.is_active = True
        new_user.save()
        self.new_user = new_user
        creator = Creator.objects.create(name='Rock Start', rating=80, logo_url='https://stackoverflow.com/')
        self.new_creator = creator
        new_game_category = GameCategory.objects.create(category_name='Horror')
        self.new_game_category = new_game_category
        new_game = Game.objects.create(name='Gta5', description='best game', rating=59,
                                       logo_url='https://stackoverflow.com/', creator=creator)
        new_game.categories.add(new_game_category)
        self.new_game = new_game

    def authorize_user(self):
        url = reverse('token_obtain_pair')
        body = {
            "email": "artem@gmail.com",
            "password": "weron1234"
        }
        response = self.client.post(url, body, format='json')

        self.access_token = response.data['access']

    def test_unauthorized_request(self):
        url = reverse('game_list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_games_list(self):
        self.authorize_user()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(reverse('game_list'), format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert response.data['count'] == 1

    def test_get_game_by_id(self):
        self.client.force_authenticate(self.new_user)
        response = self.client.get(reverse('game_details', kwargs={'id': self.new_game.id}), format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == self.new_game.id

    def test_get_creators(self):
        self.client.force_authenticate(self.new_user)

        response = self.client.get(reverse('creators_list'), format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'] is not None

    def test_get_creator_by_id(self):
        self.client.force_authenticate(self.new_user)
        response = self.client.get(reverse('creator_details', kwargs={'id': self.new_creator.id}), format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == self.new_creator.id

    def test_create_game(self):
        self.client.force_authenticate(self.new_user)

        body_data = {
            "name": "GTA5",
            "description": "Best game",
            "rating": 30,
            "logo_url": "https://stackoverflow.com/",
            "creator_pk": self.new_creator.id
        }

        response = self.client.post(reverse('game_list'), body_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'GTA5'
        assert isinstance(response.data['id'], int)

    def test_create_creator_with_error(self):
        self.client.force_authenticate(self.new_user)

        body_data = {
            "name": "",
            "foundation_date": "2021-08-08",
            "rating": 185,
            "logo_url": "https://stackoverflow.com/"
        }

        response = self.client.post(reverse('creators_list'), body_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_creator(self):
        self.client.force_authenticate(self.new_user)

        body_data = {
            "name": "Bethesda",
            "foundation_date": "",
            "rating": 85,
            "logo_url": "https://stackoverflow.com/"
        }

        response = self.client.post(reverse('creators_list'), body_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data['id'], int)
        assert response.data['name'] == body_data['name']

    def test_delete_creator(self):
        self.client.force_authenticate(self.new_user)

        response = self.client.delete(reverse('creator_details', kwargs={'id': self.new_creator.id}), format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None

    def test_delete_game(self):
        self.client.force_authenticate(self.new_user)

        response = self.client.delete(reverse('game_details', kwargs={'id': self.new_game.id}), format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None

    def test_game_update(self):
        self.client.force_authenticate(self.new_user)

        body_data = {
            "name": "GTA6",
            "description": "Best game",
            "rating": 60,
            "logo_url": "https://stackoverflow.com/",
            "creator_pk": self.new_creator.id
        }

        response = self.client.put(reverse('game_details', kwargs={'id': self.new_game.id}),
                                   data=body_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == body_data['name']

    def test_game_update_not_found(self):
        self.client.force_authenticate(self.new_user)

        body_data = {
            "name": "GTA6",
            "description": "Best game",
            "rating": 60,
            "logo_url": "https://stackoverflow.com/",
            "creator_pk": self.new_creator.id
        }

        response = self.client.put(reverse('game_details', kwargs={'id': 100}),
                                   data=body_data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_category(self):
        self.client.force_authenticate(self.new_user)

        body_data = {
            "category_name": "MMO",
            "slug": ""
        }

        response = self.client.post(reverse('game_categories'), data=body_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['slug'] == slugify(body_data['category_name'])

    def test_create_category_with_unique_error(self):
        self.client.force_authenticate(self.new_user)

        body_data = {
            "category_name": "Horror",
            "slug": ""
        }

        response = self.client.post(reverse('game_categories'), data=body_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['category_name'][0] == 'This field must be unique.'

    def test_get_category_by_id(self):
        self.client.force_authenticate(self.new_user)

        response = self.client.get(reverse('game_category', kwargs={'id': self.new_game_category.id}), format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == self.new_game_category.id

    def test_get_category_by_id_not_found(self):
        self.client.force_authenticate(self.new_user)

        response = self.client.get(reverse('game_category', kwargs={'id': 100}), format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_games_by_category(self):
        self.client.force_authenticate(self.new_user)

        response = self.client.get(reverse('get_games_by_category', kwargs={'category': self.new_game_category.slug}),
                                   format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results'][0]['categories']) != 0

    def test_get_games_by_category_not_found(self):
        self.client.force_authenticate(self.new_user)

        response = self.client.get(reverse('get_games_by_category', kwargs={'category': 'shoooter'}),
                                   format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
