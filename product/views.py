from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_list_or_404,get_object_or_404

from django.db.models import Q


from.models import Product,Review

from .serializers import ProductSerializer,ReviewSerializer

from .permissions import IsSellerOrReadOnly,IsProductOwnerOrReadOnly,IsReviewOwner



# Create your views here.
class Product_List(APIView):
    permission_classes=[IsSellerOrReadOnly]
    def get(self,request):
        products=get_list_or_404(Product)
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            product=serializer.save(seller=request.user)
            product.add_parent_categories()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
class Product_Details(APIView):
    permission_classes=[IsProductOwnerOrReadOnly]
    def get(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        serializer=ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        self.check_object_permissions(request, product)
        serializer=ProductSerializer(product,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        self.check_object_permissions(request, product)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class Review_List(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        reviews=get_list_or_404(Review,product=product)
        serializer=ReviewSerializer(reviews,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product,reviewer=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Review_Details(APIView):
    permission_classes=[IsReviewOwner]
    def put(self,request,review_pk):
        review=get_object_or_404(Review,pk=review_pk)
        self.check_object_permissions(request, review)
        serializer=ReviewSerializer(review,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,review_pk):
        review=get_object_or_404(Review,pk=review_pk)
        self.check_object_permissions(request, review)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class Search(APIView):
    def get(self,request):
        search_query = request.query_params.get('search_query', None) #search
        if search_query:
            products=Product.objects.filter(Q(name__icontains=search_query)|Q(description__icontains=search_query)|Q(category__name__icontains=search_query)).distinct()
            if not products:
                return Response({ "detail": "No products found matching your search."},status=status.HTTP_200_OK)
            category = request.query_params.get('category', None)
            min_price = request.query_params.get('min_price', None)
            max_price = request.query_params.get('max_price', None)
            if  category:
                products=products.filter(category__name=category) #filter
            if min_price:
                products=products.filter(price__gte=min_price) #filter
            if max_price:
                products=products.filter(price__lte=max_price) #filter
            if not products:
                return Response({ "detail": "No products found matching your search."},status=status.HTTP_200_OK)
        else:
            products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
        
    
    

    
    
        
               
    
    
    
    

