from django.urls import path
from rest_framework import routers

from .views import (
    StateViewSet,
    CityViewSet,
    VenueViewSet,
    dashboard_overview,
    create_venue,
)

app_name= "venues"

router = routers.DefaultRouter()
router.register(r"state", StateViewSet, basename="state")
router.register(r"city", CityViewSet, basename="city")
router.register(r"venue", VenueViewSet, basename="venue")


urlpatterns = [
   path("overview/", dashboard_overview, name="dashboard_overview"),
   path("create-venue/", create_venue, name="create_venue"),
]
# urlpatterns += router.urls