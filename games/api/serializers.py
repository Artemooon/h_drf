from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Game, Creator, GameCategory


class GameCategorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    category_name = serializers.CharField(validators=[UniqueValidator(queryset=GameCategory.objects.all())])

    class Meta:
        model = GameCategory
        fields = ['id', 'category_name', 'slug']


class GameSerializer(serializers.ModelSerializer):
    creator_pk = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(), source='creator', write_only=True
    )
    id = serializers.ReadOnlyField()

    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'rating', 'create_date', 'logo_url', 'creator', 'creator_pk',
                  'categories']
        depth = 1


class CreatorSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Creator
        fields = ['id', 'name', 'foundation_date', 'rating', 'logo_url']
