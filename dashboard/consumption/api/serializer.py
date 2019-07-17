
from rest_framework import serializers

from consumption.models import ConsumptionDailySummary, Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'area', 'tariff', 'created_at')


class ConsumptionDailySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumptionDailySummary
        fields = ('target_date', 'total_consumption', 'average_consumption')
