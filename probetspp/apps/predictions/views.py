
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.utils.mixins import APIErrorsMixin

from apps.predictions import selectors
from apps.predictions.serializers import (
    PredictionModelSerializer
)


class PredictionView(APIErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        status = serializers.IntegerField(
            required=False,
            allow_null=True
        )
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
