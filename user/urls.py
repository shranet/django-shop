from django.urls import path

from user.views import UserRegister, UserRegisterConfirm

app_name = 'user'
urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('register/confirm/', UserRegisterConfirm.as_view(), name='register-confirm')
]