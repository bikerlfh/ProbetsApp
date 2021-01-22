from django.urls import path

from apps.predictions.views import (
    PredictionView
)

urlpatterns = [
    path('', PredictionView.as_view()),
]
