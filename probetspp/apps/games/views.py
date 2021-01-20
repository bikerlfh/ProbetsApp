from rest_framework.generics import ListAPIView

from apps.games import filters
from apps.utils.mixins import APIErrorsMixin
from apps.games.models import Game, Player, League
from apps.games.serializers import (
    GameSerializer,
    PlayerSerializer,
    LeagueSerializer
)


class LeagueListView(APIErrorsMixin, ListAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class PlayerListView(APIErrorsMixin, ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filterset_class = filters.PlayerFilter


class GameListView(APIErrorsMixin, ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filterset_class = filters.GameFilter
