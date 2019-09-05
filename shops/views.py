from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CitySerializer, CityStreetSerializer
from .models import City, Street, Shop

# Create your views here.


class ListCities(APIView):

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class ListCityStreets(APIView):

    def get(self,request, pk):
        city = City.objects.filter(pk=pk)
        serializer = CityStreetSerializer(city, many=True)
        return Response(serializer.data)
