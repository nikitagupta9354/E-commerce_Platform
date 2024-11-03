from django.shortcuts import render
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from datetime import timedelta

from checkout.models import Order, OrderItem

class SalesAnalytics(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Get the current date
        today = timezone.now().date()

        # Define time periods (e.g., last 30 days, last 7 days, today)
        last_30_days = today - timedelta(days=30)
        last_7_days = today - timedelta(days=7)

        # Total sales in the last 30 days
        total_sales_30_days = OrderItem.objects.filter(
            created_at__gt=last_30_days, payment_status='Success'
        ).count()

        # Total revenue in the last 30 days
        total_revenue_30_days = OrderItem.objects.filter(
            created_at__gt=last_30_days, payment_status='Success'
        ).aggregate(total_revenue=Sum('price'))['total_revenue'] or 0
        
        # Growth in total sales compared to the previous 30 days
        previous_30_days = last_30_days - timedelta(days=30)
        previous_sales_30_days = OrderItem.objects.filter(
            created_at__gte=previous_30_days, created_at__lt=last_30_days, payment_status='Success'
        ).count()

        sales_growth_30_days = 0
        if previous_sales_30_days > 0:
            sales_growth_30_days = ((total_sales_30_days - previous_sales_30_days) / previous_sales_30_days) * 100

        # Total sales in the last 7 days
        total_sales_7_days = OrderItem.objects.filter(
            created_at__gt=last_7_days, payment_status='Success'
        ).count()

        # Total revenue in the last 7 days
        total_revenue_7_days = OrderItem.objects.filter(
            created_at__gt=last_7_days, payment_status='Success').aggregate(total_revenue=Sum('price'))['total_revenue'] or 0
        data = {
            "total_sales_30_days": total_sales_30_days,
            "total_revenue_30_days": total_revenue_30_days,
            "sales_growth_30_days": sales_growth_30_days,
            "total_sales_7_days": total_sales_7_days,
            "total_revenue_7_days": total_revenue_7_days,
        }
        
        return Response(data)


