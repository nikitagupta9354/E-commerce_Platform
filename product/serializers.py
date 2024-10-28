from rest_framework import serializers

from product.models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Product
        fields =['name','description','price','category','inventory','seller']
        
class ReviewSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(read_only=True)
    class Meta:
        model=Review
        fields=['rating','comment','created_at']
        
        
        