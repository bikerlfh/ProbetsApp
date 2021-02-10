from django_filters import rest_framework as filters
from apps.predictions.models import Prediction


class PredictionFilter(filters.FilterSet):
    league_id = filters.NumberFilter(method='league_filter')
    start_dt = filters.DateFilter(method='start_dt_filter')

    class Meta:
        model = Prediction
        fields = [
            'id', 'status',
            'league_id', 'game_id',
            'start_dt', 'player_winner_id'
        ]

    def league_filter(self, queryset, name, value):
        return queryset.filter(game__league_id=value)

    def start_dt_filter(self, queryset, name, value):
        return queryset.filter(game__start_dt__date=value)
