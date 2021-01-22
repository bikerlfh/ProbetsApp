from django.urls import path

from apps.data.views import (
    AdvanceAnalysisView
)

urlpatterns = [
    path('advance-analysis', AdvanceAnalysisView.as_view()),
]
