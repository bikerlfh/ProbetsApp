from django.urls import path

from apps.predictions.views import (
    PredictionView,
    CreateManualPredictionView
)

urlpatterns = [
    path('', PredictionView.as_view()),
    path('create/', CreateManualPredictionView.as_view()),
]
