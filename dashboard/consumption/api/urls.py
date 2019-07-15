from django.conf.urls import url, include
from rest_framework import routers

from consumption.api.views import (
    UserViewSet, ConsumptionDailySummaryChartView, ConsumptionMonthlySummaryChartView
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url('charts/consumptions/daily', ConsumptionDailySummaryChartView.as_view()),
    url('charts/consumptions/monthly', ConsumptionMonthlySummaryChartView.as_view()),
    url('', include(router.urls)),
]
