from django.urls import path
from .views import Cart_List,Cart_Details

urlpatterns = [
    path('',Cart_List.as_view(),name='cart-list'),
    path('<int:pk>',Cart_Details.as_view(),name='cart-details'),
    
]