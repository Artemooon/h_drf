import django_filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from .models import Game, Creator, GameCategory
from .serializers import GameSerializer, CreatorSerializer, GameCategorySerializer
from .services.crud_operations import create_new_game, get_games_by_category

CACHE_TTL = 60


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['^name', '=id']
    ordering_fields = ['name', 'id']

    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


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
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['^name', '=rating']
    ordering_fields = ['name', 'rating']

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
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['^category_name', 'slug']
    ordering_fields = ['name', 'id']

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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['^name', '=id']
    ordering_fields = ['name', 'id', 'rating']

    def get_queryset(self):
        slug_ = self.kwargs.get(self.lookup_url_kwarg)

        return get_games_by_category(slug_)

    @method_decorator(cache_page(CACHE_TTL * 2))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
