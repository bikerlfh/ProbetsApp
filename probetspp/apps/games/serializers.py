from django.utils import timezone
from rest_framework import serializers

from apps.utils.serializers import inline_serializer
from apps.games.models import Game


class LeagueSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.DateTimeField()


class GameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    league = serializers.SerializerMethodField()
    start_dt = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'id',
            'external_id',
            'name',
            'status',
            'start_dt',
            'league',
            'winner_id',
            'home_player_id',
            'away_player_id',
            'home_score',
            'away_score',
            'line_score'
        ]

    def get_start_dt(self, obj):
        return timezone.localtime(obj.start_dt)

    def get_name(self, obj):
        return str(obj)

    def get_league(self, obj):
        return str(obj.league)


class PlayerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    gender = serializers.IntegerField()
    stats = inline_serializer(
        fields=dict(
            total_games=serializers.IntegerField(),
            won_games=serializers.IntegerField(),
            lost_games=serializers.IntegerField(),
            won_sets=serializers.IntegerField(),
            lost_sets=serializers.IntegerField(),
            won_points=serializers.IntegerField(),
            lost_points=serializers.IntegerField(),
            back_to_win=serializers.IntegerField(),
            back_to_lose=serializers.IntegerField(),
            games_sold=serializers.IntegerField(),
            total_predictions=serializers.IntegerField(),
            won_predictions=serializers.IntegerField(),
            lost_predictions=serializers.IntegerField(),
            confidence_percentage=serializers.DecimalField(
                max_digits=5,
                decimal_places=2
            )
        )
    )
