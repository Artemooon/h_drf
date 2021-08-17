from rest_framework import serializers

from .models import Game, Creator, GameCategory


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameCategory
        fields = ['id', 'category_name', 'slug']


class GameSerializer(serializers.ModelSerializer):
    creator_pk = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(), source='creator', write_only=True
    )

    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'rating', 'create_date', 'logo_url', 'creator', 'creator_pk',
                  'categories']
        depth = 1


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ['id', 'name', 'foundation_date', 'rating', 'logo_url']
