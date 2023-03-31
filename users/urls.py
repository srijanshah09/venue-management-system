from django.urls import path, include
from users.views import (
    UserAuthView, 
)

urlpatterns = [
    path('signup/', UserAuthView.as_view({'post':'register'})),
    path('send-otp/',UserAuthView.as_view({'post':'send_otp'}),),
    path('verify-otp/',UserAuthView.as_view({'post':'verify_otp'})),
    path('request-reset-email/', UserAuthView.as_view({'post':'send_password_reset_email'}), name='request-password-reset'),
    path('password-rest/<uidb64>/<token>/', UserAuthView.as_view({'post':'reset_password'}), name='password-reset-confirm')
]
