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
        fields =['name','description','price','category','inventory','seller','currency']
        
class ReviewSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(read_only=True)
    class Meta:
        model=Review
        fields=['rating','comment','created_at']
        
    def validate_rating(self,value):
        if value<1 or value>5:
            raise serializers.ValidationError("Rating should be between 1 and 5")
        return value
    
    def validate_comment(self,value):
        if len(value)<5:
            raise serializers.ValidationError("Comment should be at least 5 characters long")
        return value
        
        
        