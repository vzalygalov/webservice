from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import City, Street, Shop


class StreetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Street
        fields = ['name']


class CityStreetSerializer(serializers.ModelSerializer):
    streets = StreetSerializer(many=True)

    class Meta:
        model = City
        fields = ['name', 'streets']


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['name']


class ShopSerializer(serializers.ModelSerializer):
    city = serializers.ReadOnlyField(source='city.name')
    street = serializers.ReadOnlyField(source='street.name')

    class Meta:
        model = Shop
        fields = ['id', 'name', 'city', 'street', 'building_number', 'opening_time', 'closing_time']
