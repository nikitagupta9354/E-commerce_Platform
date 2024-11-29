from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import CartItemSerializer
from .models import Cart,CartItem
from .permissions import IsCartItemOwner

# Create your views here.


class Cart_List(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        cartitems=CartItem.objects.filter(cart__user=request.user)
        serializer=CartItemSerializer(cartitems,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=CartItemSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            try:
                cart=Cart.objects.get(user=request.user)
            except:
                cart=Cart.objects.create(user=request.user)
            serializer.save(cart=cart)
            update_cart_total(cart)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class Cart_Details(APIView):
    permission_classes=[IsCartItemOwner]
    def put(self,request,pk):
        cartitem=get_object_or_404(CartItem,pk=pk)
        self.check_object_permissions(request, cartitem)
        serializer=CartItemSerializer(cartitem,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            update_cart_total(cartitem.cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        cartitem=get_object_or_404(CartItem,pk=pk)
        self.check_object_permissions(request, cartitem)
        cartitem.delete()
        update_cart_total(cart)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def update_cart_total(cart):
    total=0
    cartitems=CartItem.objects.filter(cart=cart)
    for item in cartitems:
        total+=(item.product.price*item.quantity)
    cart.cart_total=total
    cart.save()
    
    
    


    
    
    
    
        