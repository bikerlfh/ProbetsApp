from rest_framework.generics import ListAPIView

from apps.utils.mixins import APIErrorsMixin

from apps.predictions.models import Prediction
from apps.predictions.filters import PredictionFilter
from apps.predictions.serializers import (
    PredictionModelSerializer
)


class PredictionView(APIErrorsMixin, ListAPIView):
    queryset = Prediction.objects.all().order_by('-game__start_dt')
    serializer_class = PredictionModelSerializer
    filterset_class = PredictionFilter
