import json
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.utils.mixins import APIErrorsMixin
from apps.utils.serializers import inline_serializer

from apps.predictions import services, selectors
from apps.predictions.serializers import PredictionDataSerializer


class PredictionView(APIErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        status = serializers.IntegerField()
        league_id = serializers.IntegerField(
            required=False,
            allow_null=True
        )
        game_id = serializers.IntegerField(
            required=False,
            allow_null=True
        )
        start_dt = serializers.DateField(
            required=False,
            allow_null=True
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        game_id = serializers.IntegerField()
        status = serializers.IntegerField()
        game_data = PredictionDataSerializer()

        def __init__(self, instance=None, data=None, **kwargs):
            for ins in instance:
                ins.game_data = json.loads(ins.game_data)
            super(self.__class__, self).__init__(instance, data, **kwargs)

    def get(self, request):
        data_ = request.query_params.dict()
        in_serializer = self.InputSerializer(data=data_)
        in_serializer.is_valid(raise_exception=True)
        data = selectors.filter_prediction(
            **in_serializer.validated_data
        )
        out_serializer = self.OutputSerializer(instance=data, many=True)
        return Response(data=out_serializer.data)


class PrePredictionDataView(APIErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        league_id = serializers.IntegerField(
            required=False,
            allow_null=True
        )
        game_date = serializers.DateField(
            required=False,
            allow_null=True
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        league = serializers.CharField()
        start_dt = serializers.DateTimeField()
        winner_prediction = serializers.IntegerField()
        home_player = inline_serializer(
            fields=dict(
                id=serializers.IntegerField(),
                # name=serializers.CharField(),
                t_games=serializers.IntegerField(),
                w_games=serializers.IntegerField(),
                l_games=serializers.IntegerField(),
            )
        )
        away_player = inline_serializer(
            fields=dict(
                id=serializers.IntegerField(),
                # name=serializers.CharField(),
                t_games=serializers.IntegerField(),
                w_games=serializers.IntegerField(),
                l_games=serializers.IntegerField(),
            )
        )
        last_games_prediction = inline_serializer(
            fields=dict(
                prediction=serializers.IntegerField(),
                confidence_percentage=serializers.DecimalField(
                    max_digits=5,
                    decimal_places=2
                ),
                home_data=inline_serializer(
                    fields=dict(
                        player_id=serializers.IntegerField(),
                        percentage=serializers.DecimalField(
                            max_digits=5,
                            decimal_places=2
                        ),
                        won_games=serializers.IntegerField(),
                        lost_games=serializers.IntegerField(),
                        total_games=serializers.IntegerField(),
                    )
                ),
                away_data=inline_serializer(
                    fields=dict(
                        player_id=serializers.IntegerField(),
                        percentage=serializers.DecimalField(
                            max_digits=5,
                            decimal_places=2
                        ),
                        won_games=serializers.IntegerField(),
                        lost_games=serializers.IntegerField(),
                        total_games=serializers.IntegerField(),
                    )
                )
            )
        )
        h2h_prediction = inline_serializer(
            fields=dict(
                prediction=serializers.IntegerField(),
                confidence_percentage=serializers.DecimalField(
                    max_digits=5,
                    decimal_places=2
                ),
                home_percentage=serializers.DecimalField(
                    max_digits=5,
                    decimal_places=2
                ),
                away_percentage=serializers.DecimalField(
                    max_digits=5,
                    decimal_places=2
                ),
                last_game=serializers.DateField()
            )
        )
        h2h = inline_serializer(
            fields=dict(
                home_wins=serializers.IntegerField(),
                away_wins=serializers.IntegerField(),
                games=inline_serializer(
                    fields=dict(
                        id=serializers.IntegerField(),
                        start_dt=serializers.DateField(),
                        league_id=serializers.IntegerField(),
                        h_id=serializers.IntegerField(),
                        a_id=serializers.IntegerField(),
                        h_score=serializers.IntegerField(),
                        a_score=serializers.IntegerField(),
                        l_score=serializers.JSONField()
                    ),
                    many=True
                )
            )
        )

    def get(self, request):
        data_ = request.query_params.dict()
        in_serializer = self.InputSerializer(data=data_)
        in_serializer.is_valid(raise_exception=True)
        data = services.get_prediction_data_today(**data_)
        out_serializer = self.OutputSerializer(data=data, many=True)
        out_serializer.is_valid(raise_exception=True)
        return Response(data=out_serializer.validated_data)


class CreatePredictionView(APIErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        league_id = serializers.IntegerField(
            required=False,
            allow_null=True
        )
        game_date = serializers.DateField(
            required=False,
            allow_null=True
        )

    class OutputSerializer(serializers.Serializer):
        predictions_created = serializers.IntegerField()

    def post(self, request):
        data_ = request.data
        in_serializer = self.InputSerializer(data=data_)
        in_serializer.is_valid(raise_exception=True)
        data = services.create_predictions(**data_)
        out_serializer = self.OutputSerializer(data=data)
        out_serializer.is_valid(raise_exception=True)
        return Response(data=out_serializer.validated_data)
