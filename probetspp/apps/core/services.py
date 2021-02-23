from datetime import datetime
from typing import Dict, Any
from django.db.models import F, Count
from apps.predictions.models import Prediction
from apps.predictions.constants import PredictionStatus


def get_dashboard_data() -> Dict[str, Any]:
    now = datetime.now()
    data = {}
    won_status = PredictionStatus.WON.value
    lost_status = PredictionStatus.LOSE.value
    pending_status = PredictionStatus.DEFAULT.value
    default_status = PredictionStatus.DEFAULT.value
    p_qry = Prediction.objects.values('status').annotate(
        count=Count('status'),
        league_id=F('game__league_id'),
    ).filter(
        status__in=[
            won_status,
            lost_status,
            default_status
        ]
    ).order_by('status')
    predictions = p_qry.values(
        'count',
        'status',
        'league_id'
    )
    today_predictions = p_qry.filter(
        game__start_dt__date=now.date()
    ).values(
        'count',
        'status',
        'league_id'
    )
    won_pdt_today = sum([p['count'] for p in today_predictions
                         if p['status'] == won_status])
    lost_pdt_today = sum([p['count'] for p in today_predictions
                          if p['status'] == lost_status])
    pending_pdt_today = sum([p['count'] for p in today_predictions
                            if p['status'] == pending_status])
    won_pdt_total = sum([p['count'] for p in predictions
                         if p['status'] == won_status])
    lost_pdt_total = sum([p['count'] for p in predictions
                          if p['status'] == lost_status])
    data.update(
        today_predictions=dict(
            total_won=won_pdt_today,
            total_lost=lost_pdt_today,
            total_pending=pending_pdt_today,
            predictions=today_predictions
        ),
        history_predictions=dict(
            total_won=won_pdt_total,
            total_lost=lost_pdt_total,
            predictions=predictions
        )
    )
    return data
