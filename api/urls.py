from django.urls import path

from . import views


urlpatterns = [
    path('games/', views.GameList.as_view(), name="game_list"),
    path('game/<int:id>/', views.GameDetails.as_view(), name="game_details"),
    path('creators/', views.CreatorsList.as_view(), name="creators_list"),
    path('creator/<int:id>/', views.CreatorDetails.as_view(), name="creator_details"),
]
