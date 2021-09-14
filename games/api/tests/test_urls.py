from django.urls import reverse, resolve


class TestUrls:

    def test_game_details(self):
        path = reverse('game_details', kwargs={'id': 1})
        assert resolve(path).view_name == 'game_details'

    def test_game_list(self):
        path = reverse('game_list')
        assert resolve(path).view_name == 'game_list'

    def test_creator_details(self):
        path = reverse('creator_details', kwargs={'id': 22})
        assert resolve(path).view_name == 'creator_details'

    def test_game_categories_list(self):
        path = reverse('game_categories')
        assert resolve(path).view_name == 'game_categories'

    def test_game_category_details(self):
        path = reverse('game_category', kwargs={'id': 1})
        assert resolve(path).view_name == 'game_category'

    def test_get_games_by_categories(self):
        path = reverse('get_games_by_category', kwargs={'category': 'horror'})
        assert resolve(path).view_name == 'get_games_by_category'
