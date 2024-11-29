from rest_framework import serializers
from user.serializers import UserSerializer
from product.serializers import ProductSerializer
from .models import Address,Order,OrderItem

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'zip_code', 'country', 'is_default']

class OrderItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','price','shipping_status']
        
class OrderSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    address=AddressSerializer()
    items=OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'address', 'total_amount', 'created_at','user','items']
        
