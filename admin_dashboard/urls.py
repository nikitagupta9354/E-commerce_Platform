from django.urls import path
from .views import SalesAnalytics

urlpatterns = [
    path('sales-analytics', SalesAnalytics.as_view(), name='sales-analytics'),
]
