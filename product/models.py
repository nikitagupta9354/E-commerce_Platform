from django.db import models
from user.models import User

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
    category=models.ManyToManyField(Category)
    seller=models.ForeignKey(User,on_delete=models.CASCADE)
    inventory=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

                
    def add_parent_categories(self):
        categories=self.category.all()
        for category in categories:
            parent = category.parent
            while parent:
                self.category.add(parent)
                parent = parent.parent
        self.save()
        
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField()
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
        
                
        
            
        
    
    