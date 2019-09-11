from django.utils import timezone
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework import serializers

from .serializers import CitySerializer, CityStreetSerializer, ShopSerializer
from .models import City, Street, Shop
from .api_exceptions import StatusError, ObjectNotFound, DuplicateError, ValidationError

# Create your views here.


class ListCities(APIView):

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class ListCityStreets(APIView):

    def get(self, request, pk):
        city = City.objects.filter(pk=pk)
        serializer = CityStreetSerializer(city, many=True)
        data = serializer.data
        if data:
            return Response(data)
        raise ObjectNotFound(name='city')


class ShopView(APIView):

    def get_object(self, request, model):
        request_method = request.method

        if model is City:
            name = 'city'
        else:
            name = 'street'

        if request_method == 'POST':
            object_name = request.data.get(name)
            if not object_name:
                raise ValidationError(name=name)
        else:
            object_name = request.query_params.get(name)

        try:
            return model.objects.get(name=object_name)
        except model.DoesNotExist:
            raise ObjectNotFound(name=name)

    def get_street(self, request, city):
        name = 'street'
        streets = city.streets.all()
        given_street = request.data.get(name)
        if given_street:
            for street in streets:
                if given_street == street.name:
                    return self.get_object(request, Street)
            raise NotFound(detail={name: '{street} is not found in {city}'.format(city=city.name,
                                                                                      street=given_street)},
                           code=404)
        else:
            raise ValidationError(name=name)

    def check_opening_hours(self, request, queryset, is_open=True):
        open_shops = []
        closed_shops = []
        now = timezone.now().time()
        for shop in queryset:
            opening_time = shop.opening_time
            closing_time = shop.closing_time
            if opening_time < closing_time:
                if opening_time <= now <= closing_time:
                    open_shops.append(shop)
                else:
                    closed_shops.append(shop)
            else:
                if closing_time < now < opening_time:
                    closed_shops.append(shop)
                else:
                    open_shops.append(shop)
        if is_open:
            return open_shops
        else:
            return closed_shops

    def filter_shop_by_params(self, request, city=None, street=None, is_open=None):
        queryset = Shop.objects.all()

        if city:
            try:
                city_obj = City.objects.get(name=city)
                queryset = queryset.filter(city=city_obj)

            except City.DoesNotExist:
                raise ObjectNotFound('city')

        if street:
            queryset = queryset.filter(street__name=street)

        if is_open is not None:
            return self.check_opening_hours(request, queryset, is_open)
        return queryset

    def validate_params(self, request):
        query_params = request.query_params

        params = {'city': query_params.get('city'),
                  'street': query_params.get('street'),
                  'open': None
                  }

        for param in query_params:
            if param not in params:
                raise serializers.ValidationError('3', code='required')
        params.pop('open')

        is_open = query_params.get('open')

        if is_open:
            try:
                is_open = int(query_params.get('open'))
                if is_open in range(2):
                    params['is_open'] = is_open
                else:
                    raise StatusError
            except ValueError:
                raise StatusError
        return params

    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            city = self.get_object(request, City)
            street = self.get_street(request, city)
            try:
                serializer.save(city=city, street=street)
                response_data = {'id': serializer.data['id']}
                return Response(response_data, status=status.HTTP_200_OK)
            except IntegrityError:
                raise DuplicateError
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        if request.query_params:
            query_params = self.validate_params(request)

            shops = self.filter_shop_by_params(request, **query_params)
            serializer = ShopSerializer(shops, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            shops = Shop.objects.all()
            serializer = ShopSerializer(shops, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
