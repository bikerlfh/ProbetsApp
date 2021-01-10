from django.urls import path

from apps.predictions.views import (
    PredictionView,
    PrePredictionDataView,
    CreatePredictionView
)

urlpatterns = [
    path('', PredictionView.as_view()),
    path('get-pre-data/', PrePredictionDataView.as_view()),
    path('create/', CreatePredictionView.as_view())
]
