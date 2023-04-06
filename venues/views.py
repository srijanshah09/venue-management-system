from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import (
    State,
    City,
)
from .serializers import (
    StateSerializer,
    CitySerializer,
)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED,) 
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
        return Response(status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Default nature is sufficient"""
        queryset = self.get_queryset()
        city = get_object_or_404(queryset, pk=pk)
        city.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)