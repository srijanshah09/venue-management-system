from django.urls import path, include
from users.views import UserAuthView

urlpatterns = [
    path('signup/', UserAuthView.as_view({'post':'register'})),
]
