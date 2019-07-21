from rest_framework import viewsets
from rest_framework import filters

from consumption.models import ConsumptionDailySummary, User
from consumption.api.serializer import (
    UserSerializer, ConsumptionDailySummarySerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'area', 'tariff']


class ConsumptionDailySummaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ConsumptionDailySummary.objects.all()
    serializer_class = ConsumptionDailySummarySerializer
