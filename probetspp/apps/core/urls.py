from django.urls import path

from apps.core.views import (
    DashBoardView
)

urlpatterns = [
    path('dashboard/', DashBoardView.as_view()),
]
