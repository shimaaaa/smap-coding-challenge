# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def summary(request):
    context = {
    }
    return render(request, 'consumption/summary.html', context)


def detail(request):
    context = {
    }
    return render(request, 'consumption/detail.html', context)
