from rest_framework import serializers
from user.serializers import UserSerializer
from product.serializers import ProductSerializer
from checkout.models import Order,OrderItem
from checkout.serializers import AddressSerializer



class OrderSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    address=AddressSerializer()
    class Meta:
        model = Order
        fields = ['address','user']
        
class OrderItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    order=OrderSerializer(read_only=True)
    quantity = serializers.IntegerField(read_only=True)  
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True) 
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','price','shipping_status','order']