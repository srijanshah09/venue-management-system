from django.urls import path
from rest_framework import routers

from .views import (
    StateViewSet,
    CityViewSet,
)

router = routers.DefaultRouter()
router.register(r'state', StateViewSet, basename='state')
router.register(r'city', CityViewSet, basename='city')


urlpatterns = router.urls
