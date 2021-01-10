import json
from rest_framework import serializers

from apps.utils.serializers import inline_serializer
from apps.games.serializers import GameModelSerializer
from apps.predictions.models import Prediction


class PredictionDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    # name = serializers.CharField()
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


class PredictionModelSerializer(serializers.ModelSerializer):
    game = GameModelSerializer()
    game_data = serializers.SerializerMethodField()

    class Meta:
        model = Prediction
        fields = [
            'id',
            'status',
            'player_winner_id',
            'confidence_percentage',
            'game',
            'game_data'
        ]

    def get_game_data(self, obj):
        serializer = PredictionDataSerializer(data=json.loads(obj.game_data))
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
