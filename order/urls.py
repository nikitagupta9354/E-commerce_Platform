from django.urls import path
from .views import Buyer_Order_List,Buyer_Order_Details,Seller_Order_List,Seller_Order_Details

urlpatterns = [
    path('',Buyer_Order_List.as_view(),name='order-list'),
    path('<int:pk>',Buyer_Order_Details.as_view(),name='order-details'),
    path('seller/',Seller_Order_List.as_view(),name='order-list'),
    path('seller/<int:pk>',Seller_Order_Details.as_view(),name='order-details'),
]