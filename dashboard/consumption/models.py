# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    area = models.CharField(max_length=50)
    tariff = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'


class UserConsumptions(models.Model):
    user = models.ForeignKey(Users)
    datetime = models.DateTimeField()
    consumption = models.DecimalField(max_digits=6, decimal_places=1)

    class Meta:
        unique_together = ('user', 'datetime')
        db_table = 'user_consumptions'


class ConsumptionDailySummary(models.Model):
    target_date = models.DateField(primary_key=True)
    total_consumption = models.DecimalField(max_digits=12, decimal_places=1)
    average_consumption = models.DecimalField(max_digits=6, decimal_places=1)

    class Meta:
        db_table = 'consumption_daily_summary'
