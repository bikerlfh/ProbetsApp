from django.db.models import Q
from django_filters import rest_framework as filters
from apps.games.models import Game, Player


class PlayerFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    league_id = filters.NumberFilter(method='league_filter')

    class Meta:
        model = Player
        fields = [
            'id', 'external_id',
            'name', 'gender',
            'league_id'
        ]

    def league_filter(self, queryset, name, value):
        return queryset.filter(
            Q(home_games__league_id=value)
            | Q(away_games__league_id=value)
        ).distinct()


class GameFilter(filters.FilterSet):
    start_dt = filters.DateFilter(
        field_name="start_dt", lookup_expr='date'
    )
    external_id = filters.CharFilter(
        field_name='external_id', lookup_expr='icontains'
    )
    player_id = filters.NumberFilter(method='player_filter')
    h2h_ids = filters.CharFilter(method='h2h_filter')
    order_by = filters.OrderingFilter(
        fields=['start_dt']
    )

    class Meta:
        model = Game
        fields = ['id', 'status', 'start_dt', 'league_id', 'h2h_ids']

    def player_filter(self, queryset, name, value):
        return queryset.filter(
            Q(home_player_id=value) | Q(away_player_id=value)
        )

    def h2h_filter(self, queryset, name, value):
        ids = value.split(',')
        h_id = int(ids[0])
        a_id = int(ids[1])
        qs = queryset.filter(
            Q(home_player_id=h_id, away_player_id=a_id)
            | Q(home_player_id=a_id, away_player_id=h_id)
        )
        return qs
