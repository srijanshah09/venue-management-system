from django.urls import path
from rest_framework import routers

from .views import (
    StateViewSet,
    CityViewSet,
    VenueViewSet,
    create_venue,
)

router = routers.DefaultRouter()
router.register(r"state", StateViewSet, basename="state")
router.register(r"city", CityViewSet, basename="city")
router.register(r"venue", VenueViewSet, basename="venue")


urlpatterns = [
   path("create-venue/", create_venue, name="create_venue"),
] 
urlpatterns += router.urls