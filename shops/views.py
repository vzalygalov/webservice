from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .serializers import CitySerializer, CityStreetSerializer, ShopSerializer
from .models import City, Street, Shop

# Create your views here.


class ListCities(APIView):

    def get(self, request, format=None):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class ListCityStreets(APIView):

    def get(self, request, pk, format=None):
        city = City.objects.filter(pk=pk)
        serializer = CityStreetSerializer(city, many=True)
        data = serializer.data
        if data:
            return Response(data)
        raise NotFound(detail='city is not found', code=404)


class ShopView(APIView):

    def get_object(self, request, model):
        if model is City:
            name = 'city'
        else:
            name = 'street'
        object_name = request.data.get(name)
        try:
            return model.objects.get(name=object_name)
        except model.DoesNotExist:
            raise NotFound(detail='{name} {object_name} is not found.'.format(name=name, object_name=object_name),
                           code=404)

    def get_street(self, request, city):
        streets = city.streets.all()
        given_street = request.data['street']
        for street in streets:
            if given_street == street.name:
                return self.get_object(request, Street)
        raise NotFound(detail='street {street} is not found in {city}'.format(city=city.name, street=given_street),
                       code=404)

    def post(self, request, format=None):
        city = self.get_object(request, City)
        street = self.get_street(request, city)
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(city=city, street=street)
            response_data = {'id': serializer.data['id']}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

