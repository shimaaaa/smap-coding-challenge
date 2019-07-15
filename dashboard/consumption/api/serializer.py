
from rest_framework import serializers

from consumption.models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'area', 'tariff', 'created_at')
