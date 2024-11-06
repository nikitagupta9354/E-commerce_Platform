import csv
from io import StringIO
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from datetime import timedelta
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from checkout.models import Order, OrderItem
from ecommerce import settings
from product.models import Product

class SalesAnalytics(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Get the current date
        today = timezone.now().date()

        # Define time periods (e.g., last 30 days, last 7 days, today)
        last_30_days = today - timedelta(days=30)
        last_7_days = today - timedelta(days=7)
        
        previous_30_days_orders=OrderItem.objects.filter(
            created_at__gt=last_30_days, payment_status='Success'
        )

        # Total sales in the last 30 days
        total_sales_30_days = previous_30_days_orders.count()

        # Total revenue in the last 30 days
        total_revenue_30_days =previous_30_days_orders.aggregate(total_revenue=Sum('price'))['total_revenue'] or 0
        
        # Growth in total sales compared to the previous 30 days
        previous_30_days = last_30_days - timedelta(days=30)
        previous_sales_30_days = OrderItem.objects.filter(
            created_at__gte=previous_30_days, created_at__lt=last_30_days, payment_status='Success'
        ).count()

        sales_growth_30_days = 0
        if previous_sales_30_days > 0:
            sales_growth_30_days = ((total_sales_30_days - previous_sales_30_days) / previous_sales_30_days) * 100
            
        previous_7_days_orders = OrderItem.objects.filter(
            created_at__gt=last_7_days, payment_status='Success'
        )

        # Total sales in the last 7 days
        total_sales_7_days =previous_7_days_orders.count()

        # Total revenue in the last 7 days
        total_revenue_7_days = previous_7_days_orders.aggregate(total_revenue=Sum('price'))['total_revenue'] or 0
        data = {
            "total_sales_30_days": total_sales_30_days,
            "total_revenue_30_days": total_revenue_30_days,
            "sales_growth_30_days": sales_growth_30_days,
            "total_sales_7_days": total_sales_7_days,
            "total_revenue_7_days": total_revenue_7_days,
        }
        
        return Response(data)
    
class CustomReport(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        metric = request.data.get('metric','sales')  # e.g., sales, revenue, inventory

        # Filter orders based on the date range
        if start_date and end_date:
            orderitems = OrderItem.objects.filter(created_at__range=[start_date, end_date])

        
        if metric == 'sales':
            report_data = orderitems.aggregate(
                total_sales=Count('id'),
                total_revenue=Sum('price')
            )
            
        elif metric == 'inventory':
            report_data = dict(Product.objects.values_list('name', 'inventory'))
            

        # Creating a CSV in memory
        csv_file = StringIO()
        writer = csv.writer(csv_file)

        # Writing key-value pairs
        for key, value in report_data.items():
            writer.writerow([key, value])
        
        
        filename = f'reports/report_{timezone.now().strftime("%Y%m%d%H%M%S")}.csv'
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        # Use default storage to save the file
        default_storage.save(file_path, ContentFile(csv_file.getvalue().encode('utf-8')))

        # Construct the file URL
        file_url = request.build_absolute_uri(f'/media/{filename}')  

        # Return the file URL
        return Response({'url': file_url})
        
    



