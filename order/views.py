from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ecommerce import settings
from .serializers import OrderSerializer,OrderItemSerializer
from checkout.models import Order, OrderItem
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from product.models import Product
from .permissions import IsSeller,IsBuyer,IsProductSeller

# Create your views here.

class Buyer_Order_List(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orderitems= OrderItem.objects.filter(order__user=request.user).order_by('created_at')
        serializer = OrderItemSerializer(orderitems, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class Buyer_Order_Details(APIView):
    permission_classes = [IsBuyer]
    def get(self, request, pk):
        orderitem = get_object_or_404(OrderItem,pk=pk)
        self.check_object_permissions(request,orderitem)
        serializer = OrderItemSerializer(orderitem)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
class Seller_Order_List(APIView):
    permission_classes = [IsSeller]
    def get(self, request):
        products = Product.objects.filter(seller=request.user)
        orderitems = OrderItem.objects.filter(product__in=products).order_by('created_at')
        serializer = OrderItemSerializer(orderitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class Seller_Order_Details(APIView):
    permission_classes = [IsProductSeller]
    def get(self, request, pk):
        orderitem = get_object_or_404(OrderItem,pk=pk)
        self.check_object_permissions(request,orderitem)
        serializer = OrderItemSerializer(orderitem)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        orderitem = get_object_or_404(OrderItem,pk=pk)
        self.check_object_permissions(request,orderitem)
        customer_email=orderitem.order.user.email
        serializer = OrderItemSerializer(orderitem, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            send_mail(
            subject= f"Your order has been {serializer.data['shipping_status']}",
            message= f"Your order has been {serializer.data['shipping_status']}", 
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer_email]
            
        )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)