from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer,LoginSerializer,UserSerializer,ChangePasswordSerializer,ResetPasswordEmailSerializer,ResetPasswordSerializer
from .utils import get_tokens_for_user


# Create your views here.
class Registration(APIView):
    def post(self, request):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({'Registration Successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class Login(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(username=email,password=password)
            if user:
                token=get_tokens_for_user(user)
                return Response({'Token':token,'Message':'Login Successful'},status=status.HTTP_200_OK)
            return Response({'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
class Profile(APIView):
    permission_classes=[IsAuthenticated]
   
    def get(self, request):
        serializer=UserSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    def patch(self,request):
        serializer=UserSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ChangePassword(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer=ChangePasswordSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message':'Password Changed'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordEmail(APIView):
    def post(self, request):
        serializer=ResetPasswordEmailSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            return Response({'Message':'Password Reset Link Sent'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ResetPassword(APIView):
    def post(self, request, uid, token):
        serializer=ResetPasswordSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message':'Password Reset Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
    

    

        
        
        
        
        

