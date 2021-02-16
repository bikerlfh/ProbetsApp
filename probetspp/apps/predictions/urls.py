from django.urls import path

from apps.predictions.views import (
    PredictionView,
    NotifyPredictionView,
    CreateManualPredictionView
)

urlpatterns = [
    path('', PredictionView.as_view()),
    path('notify/', NotifyPredictionView.as_view()),
    path('create/', CreateManualPredictionView.as_view()),
]
