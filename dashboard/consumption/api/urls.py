from django.conf.urls import url, include
from rest_framework import routers

from consumption.api.views import (
    UserViewSet, ConsumptionDailySummaryViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'consumption-daily-summary', ConsumptionDailySummaryViewSet, base_name='summary')

urlpatterns = [
    url('', include(router.urls)),
]
