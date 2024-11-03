from rest_framework import serializers
from .models import Cart,CartItem
from product.models import Product
from product.serializers import ProductSerializer

        
class CartItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    class Meta:
        model=CartItem
        fields=['product','product_id','quantity']
        
    def validate(self, data):
        product_id = data.get('product_id')
        product=Product.objects.get(id=product_id.id)
        quantity = data.get('quantity')

        if quantity > product.inventory:
            raise serializers.ValidationError({
                'quantity': f"Requested quantity ({quantity}) exceeds available inventory ({product.inventory})."
            })
        return data
        
    def create(self, validated_data):
        product_id = validated_data.get('product_id')
        product=Product.objects.get(id=product_id.id)
        user=self.context['request'].user
        try:
            cartitem=CartItem.objects.get(product=product,cart__user=user)
            cartitem.quantity += validated_data['quantity']
            cartitem.save()
            return cartitem
        except:
            validated_data.pop('product_id')
            return CartItem.objects.create(**validated_data, product=product)
        