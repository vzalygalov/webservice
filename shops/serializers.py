from rest_framework import serializers
from .models import City, Street


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
