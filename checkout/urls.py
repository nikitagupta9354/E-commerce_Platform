from django.urls import path
from .views import Address_List,Address_Details,Payment_Success,Payment_Cancel,CreateCheckoutSessionView,stripe_webhook

urlpatterns = [
    path('address',Address_List.as_view(),name='address-list'),
    path('address/<int:pk>',Address_Details.as_view(),name='address-details'),
    # path('',checkout,name='checkout'),
    path('', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('payment/success',Payment_Success.as_view(),name='payment-success'),
    path('payment/cancel', Payment_Cancel.as_view(), name='payment-cancel'),
    path('webhooks/stripe',stripe_webhook,name='stripe-webhook'),
    
]