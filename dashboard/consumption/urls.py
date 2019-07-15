from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.summary),
    url(r'^summary/', views.summary),
    url(r'^detail/', views.detail),
    url(r'^api/', include('consumption.api.urls')),
]
