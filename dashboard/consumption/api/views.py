from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Sum
from django.db.models.functions import Trunc

from consumption.models import ConsumptionDailySummary, Users
from consumption.api.serializer import (
    UserSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class ConsumptionDailySummaryChartView(APIView):

    def get(self, request, format=None):
        daily_list = ConsumptionDailySummary.objects.all()
        days = [data.target_date for data in daily_list]
        total_values = [data.total_consumption for data in daily_list]

        data = {
            'days': days,
            'total_values': total_values
        }

        return Response(data=data)


class ConsumptionMonthlySummaryChartView(APIView):

    def get(self, request, format=None):
        monthly_list = ConsumptionDailySummary\
                        .objects\
                        .annotate(target_month=Trunc('target_date', 'month')).values('target_month')\
                        .annotate(total=Sum('total_consumption'))\
                        .annotate(avg=Avg('total_consumption'))

        days = [data['target_month'] for data in monthly_list]
        total_values = [data['total'] for data in monthly_list]

        data = {
            'days': days,
            'total_values': total_values
        }

        return Response(data=data)
