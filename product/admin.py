from django.contrib import admin
from .models import Category,Product,Review

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'inventory', 'created_at', 'updated_at')
    filter_horizontal = ('category',) 

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

admin.site.register(Review)
