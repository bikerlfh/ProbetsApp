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
        )[0]
        data = dict(
            id=data_['id'],
            external_id=data_['external_id'],
            name=str(game),
            league=str(game.league),
            start_dt=timezone.localtime(data_['start_dt']),
            status=data_['status'],
            h_id=game.h_id,
            a_id=game.a_id,
            h_name=str(game.home_player),
            a_name=str(game.away_player),
            h_score=game.home_score,
            a_score=game.away_score,
            h_odds=game.h_odds,
            a_odds=game.a_odds,
            home_player=data_['home_player'],
            away_player=data_['away_player'],
            prediction=prediction,
            data_game=data_game,
            h2h_games_data=data_['h2h_games_data'],
            h_last_games=data_['h_last_games'],
            a_last_games=data_['a_last_games'],
        )
        return Response(data=data)
