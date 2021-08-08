from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from .serializers import GameSerializer, CreatorSerializer

from .models import Game, Creator


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all().order_by('-create_date')
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]


class GameDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"


class CreatorsList(generics.ListCreateAPIView):
    queryset = Creator.objects.all().order_by('name')
    serializer_class = CreatorSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreatorDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
