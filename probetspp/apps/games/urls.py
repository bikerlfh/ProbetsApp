from django.urls import path

from apps.games.views import (
    GameListView,
    LeagueListView,
    PlayerListView,
    GameDetailView
)

urlpatterns = [
    path('', GameListView.as_view()),
    path('<int:game_id>/', GameDetailView.as_view()),
    path('league/', LeagueListView.as_view()),
    path('player/', PlayerListView.as_view()),
]
