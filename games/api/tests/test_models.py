import pytest
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:

    def test_game_in_list(self):
        game = mixer.blend('api.Game', name='GTA5')
        assert game.name == 'GTA5'