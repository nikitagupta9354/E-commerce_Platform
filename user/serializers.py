from rest_framework import serializers
from .models import User
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model= User
        fields=['email','first_name','last_name','phone_number','role','password','confirm_password']
        extra_kwargs = {
        'password':{'write_only':True}
        }
        
    def validate(self, attrs):
        password=attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        if password!=confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self,validated_data):
        del validated_data['confirm_password']
        return User.objects.create_user(** validated_data)
    
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)
    class Meta:
        model= User
        fields=['email','password']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','email','first_name','last_name','phone_number','role']
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password= serializers.CharField(style={'input_type':'password'}, write_only=True)
    new_password= serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_new_password=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model= User
        fields=['old_password','new_password','confirm_new_password']
        
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"Old password is not correct."})
        
    def validate(self, attrs):
        new_password=attrs.get('new_password')
        confirm_new_password=attrs.get('confirm_new_password')
        if new_password!=confirm_new_password:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
        
    def save(self):
        user = self.context['request'].user
        password=self.validated_data['new_password']
        user.set_password(password)
        user.save()
        
class ResetPasswordEmailSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)
    class Meta:
        model= User
        fields=['email']
        
    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError({"You are not a registered user."})
        uid=urlsafe_base64_encode(force_bytes(user.id))
        token=PasswordResetTokenGenerator().make_token(user)
        link='http://localhost:3000/api/user/reset/'+uid+'/'+token
        send_mail('Password Reset', link, settings.DEFAULT_FROM_EMAIL, [user.email])
        return value
    
class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password= serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_new_password=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model= User
        fields=['new_password','confirm_new_password']
    
    def validate(self, attrs):
        new_password=attrs.get('new_password')
        confirm_new_password=attrs.get('confirm_new_password')
        if new_password!=confirm_new_password:
            raise serializers.ValidationError("Passwords do not match")
        try:
            id=smart_str(urlsafe_base64_decode(self.context.get('uid')))
            user=User.objects.get(id=id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid UID')
        
        token=self.context.get('token')
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError('Token is invalid or expired')
        
        return attrs
    
    def save(self):
        id=smart_str(urlsafe_base64_decode(self.context.get('uid')))
        user=User.objects.get(id=id)
        password=self.validated_data['new_password']
        user.set_password(password)
        user.save()
    

        
        
    
    
        
    
    
        
        
        
        
    
        
    