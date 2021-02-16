from decimal import Decimal
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.utils.mixins import APIErrorsMixin

from apps.predictions.constants import PredictionType
from apps.predictions.models import Prediction
from apps.predictions.filters import PredictionFilter
from apps.predictions.serializers import (
    PredictionModelSerializer
)
from apps.predictions import services, communications


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

        prediction = services.create_prediction(
            **validated_data,
            confidence=Decimal(80),
            type_=PredictionType.MANUAL.value
        )
        if not prediction:
            raise ValidationError('error creating prediction')
        communications.notify_prediction(prediction=prediction)
        return Response()


class NotifyPredictionView(APIErrorsMixin, APIView):
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        prediction_id = serializers.IntegerField()
        to = serializers.CharField(required=False)

    def post(self, request):
        print(request.data)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        communications.notify_prediction(
            **validated_data
        )
        return Response(data={})
