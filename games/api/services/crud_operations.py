from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from ..models import Game, Creator, GameCategory


def create_new_game(data):
    creator = Creator.objects.get(id=data.get('creator_pk', None))
    new_game = Game.objects.create(name=data.get('name', ''),
                                   description=data.get('description', ''),
                                   rating=data.get('rating', 0),
                                   logo_url=data.get('logo_url', ''),
                                   creator=creator)

    for category in data.get('categories', ''):
        if GameCategory.objects.filter(slug=category['slug']).exists():
            game_category = GameCategory.objects.get(slug=category['slug'])
            new_game.categories.add(game_category)
        else:
            return Response({'message': 'Category with some introduced slug not found'},
                            status=status.HTTP_400_BAD_REQUEST)


def get_games_by_category(slug_):
    category = get_object_or_404(GameCategory, slug=slug_)
    games_by_category = Game.objects.filter(categories=category)
    return games_by_category
