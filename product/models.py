from django.db import models
from ecommerce import settings
from user.models import User
from django.core.mail import send_mail

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
    
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image=models.ImageField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3,default='inr')
    category=models.ManyToManyField(Category)
    seller=models.ForeignKey(User,on_delete=models.CASCADE)
    inventory=models.IntegerField()
    stripe_product_id=models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        message=f'Restock your {self.name}'
        if  self.inventory<=10:
            send_mail(subject='Inventory Low Alert!',
                      message=message,
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[self.seller.email],
                      )


                
    def add_parent_categories(self):
        categories=self.category.all()
        for category in categories:
            parent = category.parent
            while parent:
                self.category.add(parent)
                parent = parent.parent
        self.save()
        
class Cost(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    stripe_price_id = models.CharField(max_length=100, unique=True)  
    cost = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    currency = models.CharField(max_length=3, default='inr') 
    
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField()
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
        
                
        
            
        
    
    