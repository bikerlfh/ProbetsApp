from django.utils import timezone
from rest_framework import serializers

from apps.games.models import Game


class GameModelSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    league = serializers.SerializerMethodField()
    start_dt = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'id',
            'external_id',
            'status',
            'start_dt',
            'name',
            'league',
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
