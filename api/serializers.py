from rest_framework import serializers

from .models import Game, Creator


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'rating', 'create_date', 'logo_url', 'creator']


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ['id', 'name', 'foundation_date', 'rating', 'logo_url']
