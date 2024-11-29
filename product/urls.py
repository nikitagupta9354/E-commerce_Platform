from django.urls import path
from .views import Product_List,Product_Details,Review_List,Review_Details,Search

urlpatterns = [
    path('',Product_List.as_view(),name='product-list'),
    path('<int:pk>',Product_Details.as_view(),name='product-details'),
    path('<int:pk>/reviews',Review_List.as_view(),name='review-list'),
    path('reviews/<int:review_pk>',Review_Details.as_view(),name='review-details'),
    path('search',Search.as_view(),name='search')
    
]