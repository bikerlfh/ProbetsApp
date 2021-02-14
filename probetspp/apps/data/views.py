
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.utils.mixins import APIErrorsMixin

from apps.data.serializers import AnalysisSerializer
from apps.data import services


class AdvanceAnalysisView(APIErrorsMixin, APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        game_id = serializers.IntegerField(
            required=False,
            allow_null=True
        )
        status = serializers.IntegerField(
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
        data = services.get_advance_analysis_data(
            **in_serializer.validated_data
        )
        out_serializer = AnalysisSerializer(data=data, many=True)
        out_serializer.is_valid(raise_exception=True)
        return Response(data=out_serializer.data)
