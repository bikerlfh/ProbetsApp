from django.contrib import admin
from apps.games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    readonly_fields = [
        'external_id',
        'league',
        'home_player',
        'away_player',
        'start_dt',
        'home_score',
        'away_score',
        'line_score'
    ]
    list_display = [
        'name',
        'league',
        'home_player',
        'away_player',
        'start_dt',
        'status',
        'home_score',
        'away_score'
    ]

    def name(self, obj):
        return str(obj)
