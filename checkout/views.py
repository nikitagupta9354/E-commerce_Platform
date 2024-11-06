from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from cart.models import Cart, CartItem
from ecommerce import settings
from user.models import User
from .serializers import AddressSerializer,OrderSerializer
from .models import Address, Order,OrderItem
from .permissions import IsAddressOwner
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import json
from django.core.mail import send_mail
from product.models import Product
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.


class Address_List(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer=AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Address_Details(APIView):
    permission_classes=[IsAddressOwner]
    def put(self, request, pk):
        address = get_object_or_404(Address,pk=pk)
        self.check_object_permissions(request, address)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = get_object_or_404(Address,pk=pk)
        self.check_object_permissions(request, address)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


# def checkout(request):
#     return render(request, 'checkout.html')


class Payment_Success(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        order = Order.objects.filter(user=request.user).order_by('created_at').first() 
        serializer=OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class Payment_Cancel(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        return Response({'Error': 'Payment Failed'}, status=status.HTTP_400_BAD_REQUEST)
        

class CreateCheckoutSessionView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        selected_address_id = request.data.get('address_id')
        cart_items = CartItem.objects.filter(cart__user=request.user)
        line_items = []
        for item in cart_items:
            cost = item.product.cost_set.first()# Assuming a product has one cost associated
            line_items.append({
                'price': cost.stripe_price_id,
                'quantity': item.quantity,
            })
            
            
        
        DOMAIN = f"http://{request.get_host()}"
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                metadata={
                    'user_id': request.user.id,
                    'address_id': str(selected_address_id),  # Store address ID for lookup later
                },
                success_url=f"{DOMAIN}/api/checkout/payment/success",
                cancel_url=f"{DOMAIN}/api/checkout/payment/cancel",
            )
            return Response(checkout_session.url, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_KEY  

    try:
        event = stripe.Webhook.construct_event( 
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']  
        customer_email = session['customer_details']['email']
        address_id = session['metadata']['address_id']
        address = Address.objects.get(id=address_id)
        user_id = session['metadata']['user_id']
        user = User.objects.get(id=user_id)
        # cart=Cart.objects.get(user=user)
        # cart_items = CartItem.objects.filter(cart=cart)
        cart = Cart.objects.prefetch_related('cartitem_set').get(user=user)
        cart_items = cart.cartitem_set.all()
        order=Order.objects.create(user=user,address=address,payment_status='Success',total_amount=cart.cart_total)#create order after successful payment
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price*cart_item.quantity, 
                payment_status='Success',
            )
        # cart_items.delete()
        # cart.delete()
        # orderitem=OrderItem.objects.filter(order=order)
        for i in order.orderitem_set.all():
            i.product.inventory-=i.quantity
            i.product.save()
        
        subject="Your payment is successful"
        text_content = f"Thank you for your purchase, {order.user.first_name}. Your order ID is {order.id}."
        from_email=settings.DEFAULT_FROM_EMAIL
        recipient_list=[customer_email]
        email = EmailMultiAlternatives(
        subject, text_content, from_email, recipient_list   #send mail with receipt
        )
        html_content = render_to_string('receipt_html.html', {'order': order,'orderitem':orderitem})
        email.attach_alternative(html_content, "text/html")
        email.send()
        return JsonResponse({'status': 'success'})
    
    if event['type'] == 'payment_intent.payment_failed':
        return JsonResponse({'status': 'failed'})
    if event['type'] == 'charge.failed':
        return JsonResponse({'status': 'failed'})
    return JsonResponse({'status': 'unhandled_event'})


