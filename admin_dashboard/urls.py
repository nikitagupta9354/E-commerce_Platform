from django.urls import path
from .views import SalesAnalytics,CustomReport

urlpatterns = [
    path('sales-analytics', SalesAnalytics.as_view(), name='sales-analytics'),
    path('custom-reports', CustomReport.as_view(), name='custom-reports'),
]
