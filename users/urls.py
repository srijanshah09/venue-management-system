from django.urls import path, include
from users.views import (
    UserAuthView, 
)

urlpatterns = [
    path('signup/', UserAuthView.register, name='register'),
    path('send-otp/',UserAuthView.send_otp, name='send-otp'),
    path('verify-otp/',UserAuthView.verify_otp, name='verify-otp'),
    path('request-reset-email/', UserAuthView.send_password_reset_email, name='request-password-reset'),
    path('password-rest/<uidb64>/<token>/', UserAuthView.reset_password, name='password-reset-confirm')
]
