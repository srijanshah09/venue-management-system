from django.urls import path, include
from users.views import UserAuthView

urlpatterns = [
    path('signup/', UserAuthView.as_view({'post':'register'})),
    path('send-otp/',UserAuthView.as_view({'post':'send_otp'}),),
    path('verify-otp/',UserAuthView.as_view({'post':'verify_otp'})),
]
