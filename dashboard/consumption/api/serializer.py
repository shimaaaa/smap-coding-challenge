
from rest_framework import serializers

from consumption.models import ConsumptionDailySummary, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'area', 'tariff', 'created_at')


class ConsumptionDailySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumptionDailySummary
        fields = ('target_date', 'total_value', 'average_value')
