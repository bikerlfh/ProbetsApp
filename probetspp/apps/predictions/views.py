from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.utils.mixins import APIErrorsMixin

from apps.predictions.models import Prediction
from apps.predictions.filters import PredictionFilter
from apps.predictions.serializers import (
    PredictionModelSerializer
)


class PredictionView(APIErrorsMixin, ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Prediction.objects.all().order_by('-game__start_dt')
    serializer_class = PredictionModelSerializer
    filterset_class = PredictionFilter
