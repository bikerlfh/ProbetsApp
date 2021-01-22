from django.contrib import admin
from apps.data.models import DataWeights, DataGame, AcceptanceValue


@admin.register(DataWeights)
class DataWeightsAdmin(admin.ModelAdmin):
    list_display = [
        'player',
        'wt_games',
        'wt_sets',
        'wt_points',
        'wt_games_sold',
        'wt_predictions',
        'wt_h2h',
        'wt_last_games',
        'wt_direct_opponents'
    ]


@admin.register(AcceptanceValue)
class AcceptanceValueAdmin(admin.ModelAdmin):
    list_display = [
        'p_wt_diff',
        'h2h_wt_diff',
        'lg_wt_diff',
        'd_opp_wt_diff',
        'is_active'
    ]


@admin.register(DataGame)
class DataGameAdmin(admin.ModelAdmin):
    readonly_fields = [
        'game',
        'p_wt_diff',
        'h2h_wt_diff',
        'lg_wt_diff',
        'd_opp_wt_diff',
        'confidence'
    ]
    list_display = [
        'game',
        'h_wt_score',
        'a_wt_score',
        'h_h2h_wt_score',
        'a_h2h_wt_score',
        'h_lg_wt_score',
        'a_lg_wt_score',
        'h_d_opp_wt_score',
        'a_d_opp_wt_score'
    ]

    def p_wt_diff(self, obj):
        return obj.acceptance_value.p_wt_diff

    def h2h_wt_diff(self, obj):
        return obj.acceptance_value.h2h_wt_diff

    def lg_wt_diff(self, obj):
        return obj.acceptance_value.lg_wt_diff

    def d_opp_wt_diff(self, obj):
        return obj.acceptance_value.d_opp_wt_diff

    p_wt_diff.short_description = 'min player wt diff'
    h2h_wt_diff.short_description = 'min h2h wt diff'
    lg_wt_diff.short_description = 'min last games wt diff'
    d_opp_wt_diff.short_description = 'min direct opponents wt diff'
