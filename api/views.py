from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from .models import Game, Creator, GameCategory
from .serializers import GameSerializer, CreatorSerializer, GameCategorySerializer

CACHE_TTL = 60


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all().order_by('-create_date')
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = GameSerializer(data=request.data)

        if serializer.is_valid():
            data = request.data

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
                    return Response({'Bad Request': 'Category with some introduced slug not found'},
                                    status=status.HTTP_400_BAD_REQUEST)

            serializer = GameSerializer(new_game)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class GameDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        id_ = self.kwargs['id']
        return Game.objects.filter(id=id_)


class CreatorsList(generics.ListCreateAPIView):
    queryset = Creator.objects.all().order_by('name')
    serializer_class = CreatorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL * 2))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CreatorDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreatorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        id_ = self.kwargs['id']
        return Creator.objects.filter(id=id_)


class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all().order_by('category_name')
    serializer_class = GameCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL * 2))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class GameCategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        id_ = self.kwargs['id']
        return GameCategory.objects.filter(id=id_)


class GamesByCategory(generics.ListAPIView):
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "category"

    def get_queryset(self):
        slug_ = self.kwargs.get(self.lookup_url_kwarg)
        category = get_object_or_404(GameCategory, slug=slug_)
        games_by_category = Game.objects.filter(categories=category)
        return games_by_category

    @method_decorator(cache_page(CACHE_TTL * 2))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)