from django.db import models

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    cart_total=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    def __str__(self):
        return f"{self.user.email}'s Cart"
    

class CartItem(models.Model):
    cart=models.ForeignKey('Cart',on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.email}'s Cart"
   


