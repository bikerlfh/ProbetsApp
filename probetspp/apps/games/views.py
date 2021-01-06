from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.utils.mixins import APIErrorsMixin
from apps.utils.serializers import inline_serializer

from apps.games import services, selectors


class LeagueView(APIErrorsMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.DateTimeField()

    def get(self, request):
        data = selectors.get_all_leagues()
        out_serializer = self.OutputSerializer(instance=data, many=True)
        return Response(data=out_serializer.data)


class PlayerView(APIErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        league_id = serializers.IntegerField(
            required=False
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.DateTimeField()

    def get(self, request):
        params = request.query_params.dict()
        in_serializer = self.InputSerializer(data=params)
        in_serializer.is_valid(raise_exception=True)
        data = selectors.filter_player(**params)
        out_serializer = self.OutputSerializer(instance=data, many=True)
        return Response(data=out_serializer.data)


class LastPlayerGames(APIErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        player_id = serializers.IntegerField(
            required=True
        )
        limit = serializers.IntegerField(
            required=False
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        start_dt = serializers.DateTimeField()
        status = serializers.IntegerField()
        league_id = serializers.IntegerField()
        home_player = inline_serializer(
            fields=dict(
                id=serializers.IntegerField(),
                name=serializers.CharField()
            )
        )
        away_player = inline_serializer(
            fields=dict(
                id=serializers.IntegerField(),
                name=serializers.CharField()
            )
        )
        home_score = serializers.IntegerField()
        away_score = serializers.IntegerField()
        line_score = serializers.JSONField()

    def get(self, request):
        data_ = request.query_params.dict()
        in_serializer = self.InputSerializer(data=data_)
        in_serializer.is_valid(raise_exception=True)
        validate_data = in_serializer.validated_data
        data = selectors.filter_last_games_by_player_id(**validate_data)
        out_serializer = self.OutputSerializer(instance=data, many=True)
        return Response(data=out_serializer.data)


class GameView(APIErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        league_id = serializers.IntegerField(
            required=False
        )
        start_dt = serializers.DateField(
            required=False
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        start_dt = serializers.DateTimeField()
        status = serializers.IntegerField()
        league_id = serializers.IntegerField()
        home_player = inline_serializer(
            fields=dict(
                id=serializers.IntegerField(),
                name=serializers.CharField()
            )
        )
        away_player = inline_serializer(
            fields=dict(
                id=serializers.IntegerField(),
                name=serializers.CharField()
            )
        )
        home_score = serializers.IntegerField()
        away_score = serializers.IntegerField()
        line_score = serializers.JSONField()

    def post(self, request):
        in_serializer = self.InputSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = services.get_games(**request.data)
        out_serializer = self.OutputSerializer(instance=data, many=True)
        return Response(data=out_serializer.data)
