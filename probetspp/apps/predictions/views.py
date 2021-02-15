from decimal import Decimal
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.utils.mixins import APIErrorsMixin

from apps.predictions.constants import PredictionType
from apps.predictions.models import Prediction
from apps.predictions.filters import PredictionFilter
from apps.predictions.serializers import (
    PredictionModelSerializer
)
from apps.predictions import services


class PredictionView(APIErrorsMixin, ListAPIView):
    queryset = Prediction.objects.all().order_by('-game__start_dt')
    serializer_class = PredictionModelSerializer
    filterset_class = PredictionFilter


class CreateManualPredictionView(APIErrorsMixin, APIView):
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        game_id = serializers.IntegerField()
        player_winner_id = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        data = services.create_prediction(
            **validated_data,
            confidence=Decimal(80),
            type_=PredictionType.MANUAL.value
        )
        return Response(data=dict(id=data.id))
