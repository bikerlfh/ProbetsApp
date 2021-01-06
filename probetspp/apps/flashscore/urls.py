from django.urls import path

from apps.flashscore.views import LoadEventsView, ReadEventsView

urlpatterns = [
    path('load-events/', LoadEventsView.as_view()),
    path('read-events/', ReadEventsView.as_view()),
]
