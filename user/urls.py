from django.urls import path
from .views import Registration,Login,Profile,ChangePassword,ResetPasswordEmail,ResetPassword
   

urlpatterns = [
    path('register/',Registration.as_view(),name='register' ),
    path('login/',Login.as_view(),name='login' ),
    path('profile/',Profile.as_view(),name='profile' ),
    path('changepassword/',ChangePassword.as_view(),name='change-password' ),
    path('resetpasswordemail/',ResetPasswordEmail.as_view(),name='reset-password-email'),
    path('resetpassword/<uidb64>/<token>/',ResetPassword.as_view(),name='reset-password')
]