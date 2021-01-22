from typing import Dict, Any, List
from rest_framework import serializers

from apps.utils.decimal import format_decimal_to_n_places


class AnalysisSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    h_id = serializers.IntegerField()
    a_id = serializers.IntegerField()
    h_wt_score = serializers.DecimalField(
        max_digits=18,
        decimal_places=2
    )
    a_wt_score = serializers.DecimalField(
        max_digits=18,
        decimal_places=2
    )
    t_h2h = serializers.IntegerField()
    h_h2h_wins = serializers.IntegerField()
    a_h2h_wins = serializers.IntegerField()
    h_h2h_wt_score = serializers.DecimalField(
        max_digits=18,
        decimal_places=2
    )
    a_h2h_wt_score = serializers.DecimalField(
        max_digits=22,
        decimal_places=2
    )
    h_lg_wt_score = serializers.DecimalField(
        max_digits=18,
        decimal_places=2
    )
    a_lg_wt_score = serializers.DecimalField(
        max_digits=18,
        decimal_places=2
    )
    h_d_opp_wt_score = serializers.DecimalField(
        max_digits=18,
        decimal_places=2
    )
    a_d_opp_wt_score = serializers.DecimalField(
        max_digits=18,
        decimal_places=2
    )
    winner_id = serializers.IntegerField()
    confidence = serializers.DecimalField(
        max_digits=18,
        decimal_places=2
    )

    def __init__(
        self,
        instance=None,
        data: List[Dict[str, Any]] = None, **kwargs
    ):
        for d_ in data:
            d_['h_wt_score'] = format_decimal_to_n_places(
                value=d_['h_wt_score']
            )
            d_['a_wt_score'] = format_decimal_to_n_places(
                value=d_['a_wt_score']
            )
            d_['h_h2h_wt_score'] = format_decimal_to_n_places(
                value=d_['h_h2h_wt_score']
            )
            d_['a_h2h_wt_score'] = format_decimal_to_n_places(
                value=d_['a_h2h_wt_score']
            )
            d_['h_lg_wt_score'] = format_decimal_to_n_places(
                value=d_['h_lg_wt_score']
            )
            d_['a_lg_wt_score'] = format_decimal_to_n_places(
                value=d_['a_lg_wt_score']
            )
            d_['h_d_opp_wt_score'] = format_decimal_to_n_places(
                value=d_['h_d_opp_wt_score']
            )
            d_['a_d_opp_wt_score'] = format_decimal_to_n_places(
                value=d_['a_d_opp_wt_score']
            )
            d_['confidence'] = format_decimal_to_n_places(
                value=d_['confidence']
            )
        super(AnalysisSerializer, self).__init__(instance, data, **kwargs)
