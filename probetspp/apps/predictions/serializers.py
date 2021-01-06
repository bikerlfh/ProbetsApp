from rest_framework import serializers

from apps.utils.serializers import inline_serializer


class PredictionDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    league = serializers.CharField()
    start_dt = serializers.DateTimeField()
    winner_prediction = serializers.IntegerField()
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
    home_player = inline_serializer(
        fields=dict(
            id=serializers.IntegerField(),
            name=serializers.CharField(),
            total_games=serializers.IntegerField(),
            won_games=serializers.IntegerField(),
            lost_games=serializers.IntegerField(),
        )
    )
    away_player = inline_serializer(
        fields=dict(
            id=serializers.IntegerField(),
            name=serializers.CharField(),
            total_games=serializers.IntegerField(),
            won_games=serializers.IntegerField(),
            lost_games=serializers.IntegerField(),
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
                    home_player_id=serializers.IntegerField(),
                    away_player_id=serializers.IntegerField(),
                    home_score=serializers.IntegerField(),
                    away_score=serializers.IntegerField(),
                    line_score=serializers.JSONField()
                ),
                many=True
            )
        )
    )
