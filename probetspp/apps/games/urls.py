from django.urls import path

from apps.games.views import (
    GameView,
    LeagueView,
    PlayerView,
    LastPlayerGames
)

urlpatterns = [
    path('', GameView.as_view()),
    path('league/', LeagueView.as_view()),
    path('player/', PlayerView.as_view()),
    path('player/games/', LastPlayerGames.as_view())
]
