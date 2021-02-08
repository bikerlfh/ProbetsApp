from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.utils.mixins import APIErrorsMixin
from apps.data import selectors as data_selectors
from apps.predictions import selectors as predictions_selectors
from apps.games import filters
from apps.games.models import Game, Player, League
from apps.games.serializers import (
    GameSerializer,
    PlayerSerializer,
    LeagueSerializer
)
from apps.games import services, selectors


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


class GameDetailView(APIErrorsMixin, APIView):
    def get(self, request, game_id: int):
        game_qry = selectors.filter_game_by_id(
            game_id=game_id
        )
        if not game_qry.exists():
            raise ValidationError('game does not exists')
        game = game_qry.first()
        prediction = predictions_selectors.filter_prediction_by_game_id(
            game_id=game_id
        ).values(
            'player_winner_id',
            'status',
            'confidence'
        ).first()
        data_game = data_selectors.filter_data_game_by_game_id(
            game_id=game_id
        ).first()
        data_ = services.get_games_data_to_predict(
            game_id=game_id,
            last_games_limit=10
        )
        data = dict(
            name=str(game),
            h_id=game.h_id,
            a_id=game.a_id,
            h_name=str(game.home_player),
            a_name=str(game.away_player),
            h_odds=game.h_odds,
            a_odds=game.a_odds,
            league=str(game.league),
            prediction=prediction,
            data_game=data_game,
        )
        data.update(**data_[0])
        data.update(
            start_dt=timezone.localtime(data['start_dt'])
        )
        return Response(data=data)
