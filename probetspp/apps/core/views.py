from rest_framework.views import APIView
from rest_framework.response import Response
from apps.utils.mixins import APIErrorsMixin
from apps.core import services


class DashBoardView(APIErrorsMixin, APIView):
    def get(self, request):
        data = services.get_dashboard_data()
        return Response(data=data)
