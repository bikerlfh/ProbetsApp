from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.utils.mixins import APIErrorsMixin

from apps.flashscore import services


class ReadEventsView(APIErrorsMixin, APIView):

    class InputSerializer(serializers.Serializer):
        file_date = serializers.DateField(
            required=False
        )

    class OutputSerializer(serializers.Serializer):
        league = serializers.CharField()
        external_id = serializers.CharField()
        start_at = serializers.DateTimeField()
        stage = serializers.CharField(
            required=False,
            allow_null=True
        )
        home_player = serializers.CharField()
        away_player = serializers.CharField()
        home_score = serializers.IntegerField()
        away_score = serializers.IntegerField()
        line_score = serializers.JSONField(
            required=False,
            allow_null=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_ = serializer.validated_data
        file_date = data_.get('file_date')
        if file_date:
            data = services.read_events_from_html_file(
                file_date=file_date
            )
        else:
            data = services.read_events_web_driver()
        out_serializer = self.OutputSerializer(data=data, many=True)
        out_serializer.is_valid(raise_exception=True)
        return Response(data=out_serializer.validated_data)


class LoadEventsView(APIErrorsMixin, APIView):

    class InputSerializer(serializers.Serializer):
        file_date = serializers.DateField(
            required=False
        )

    class OutputSerializer(serializers.Serializer):
        events_created = serializers.IntegerField()
        events_updated = serializers.IntegerField()

    def get(self, request):
        data_ = request.query_params.dict()
        serializer = self.InputSerializer(data=data_)
        serializer.is_valid(raise_exception=True)
        data_ = serializer.validated_data
        file_date = data_.get('file_date')
        data = services.load_events(
            file_date=file_date
        )
        out_serializer = self.OutputSerializer(data=data)
        out_serializer.is_valid(raise_exception=True)
        return Response(data=out_serializer.validated_data)
