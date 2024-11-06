from django.db import models
from user.models import User
from cart.models import Cart
from product.models import Product

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    
   
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES=[
        ('Success','Success'),
        ('Refund Demanded','Refund Demanded'),
        ('Refund Processed','Refund Processed'),
        ('Partially Refunded','Partially Refunded'),
    ]
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    address=models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class OrderItem(models.Model):
    CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
    ]
    STATUS_CHOICES=[
        ('Success','Success'),
        ('Refund Demanded','Refund Demanded'),
        ('Refund Processed','Refund Processed'),
    ]
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_status=models.CharField(max_length=20, choices=CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
