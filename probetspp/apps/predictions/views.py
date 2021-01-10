
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.utils.mixins import APIErrorsMixin
from apps.utils.serializers import inline_serializer

from apps.predictions import services, selectors
from apps.predictions.serializers import (
    PredictionModelSerializer,
    PredictionDataSerializer
)


class PredictionView(APIErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        status = serializers.IntegerField()
        league_id = serializers.IntegerField(
            required=False,
            allow_null=True
        )
        game_id = serializers.IntegerField(
            required=False,
            allow_null=True
        )
        start_dt = serializers.DateField(
            required=False,
            allow_null=True
        )

    def get(self, request):
        data_ = request.query_params.dict()
        in_serializer = self.InputSerializer(data=data_)
        in_serializer.is_valid(raise_exception=True)
        data = selectors.filter_prediction(
            **in_serializer.validated_data
        )
        out_serializer = PredictionModelSerializer(instance=data, many=True)
        return Response(data=out_serializer.data)


class PrePredictionDataView(APIErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        league_id = serializers.IntegerField(
            required=False,
            allow_null=True
        )
        game_date = serializers.DateField(
            required=False,
            allow_null=True
        )

    def get(self, request):
        data_ = request.query_params.dict()
        in_serializer = self.InputSerializer(data=data_)
        in_serializer.is_valid(raise_exception=True)
        data = services.get_prediction_data_today(**data_)
        out_serializer = PredictionDataSerializer(data=data, many=True)
        out_serializer.is_valid(raise_exception=True)
        return Response(data=out_serializer.validated_data)


class CreatePredictionView(APIErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        league_id = serializers.IntegerField(
            required=False,
            allow_null=True
        )
        game_date = serializers.DateField(
            required=False,
            allow_null=True
        )

    class OutputSerializer(serializers.Serializer):
        predictions_created = serializers.IntegerField()

    def post(self, request):
        data_ = request.data
        in_serializer = self.InputSerializer(data=data_)
        in_serializer.is_valid(raise_exception=True)
        data = services.create_predictions(**data_)
        out_serializer = self.OutputSerializer(data=data)
        out_serializer.is_valid(raise_exception=True)
        return Response(data=out_serializer.validated_data)
