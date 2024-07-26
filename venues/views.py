from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .serializers import (
    StateSerializer,
    CitySerializer,
    VenueSerializer,
)
from .forms import VenueCreationForm

# Create your views here.
class StateViewSet(viewsets.ModelViewSet):

    model = State
    queryset = State.objects.filter(is_active=True)
    serializer_class = StateSerializer


class CityViewSet(viewsets.ViewSet):
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.filter(is_active=True)

    def create(self, request, format=None):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        city = get_object_or_404(queryset, pk=pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)

    def update(self, request, pk, format=None):
        queryset = self.get_queryset()
        city = get_object_or_404(queryset, pk=pk)
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(city, serializer.data)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = self.get_queryset()
        city = get_object_or_404(queryset, pk=pk)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VenueViewSet(viewsets.ModelViewSet):

    model = Venue
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

    def get_queryset(self):
        return Venue.objects.filter(is_active=True)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        venue = get_object_or_404(queryset, pk=pk)
        serializer = VenueSerializer(venue)
        return Response(serializer.data)

    def update(self, request, pk, format=None):
        queryset = self.get_queryset()
        venue = get_object_or_404(queryset, pk=pk)
        serializer = VenueSerializer(data=request.data)

        if serializer.is_valid():
            serializer.update(venue, serializer.data)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@login_required
def dashboard_overview(request):
    return render(request, "venues/overview.html")

@login_required
def create_venue(request):
    form = VenueCreationForm()
    if request.method == "POST":
        form = VenueCreationForm(request.POST)
        if form.is_valid:
            form_object = form.save(commit=False)
            form_object.owner = request.user
            form_object.save()
            return redirect(reverse("venues:dashboard_overview"))
    context = {
        "form": form
    }
    return render(request, "venues/create_venue.html", context)