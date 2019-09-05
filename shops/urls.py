from django.urls import path, re_path

from . import views

urlpatterns = [
    path('city/<int:pk>/street',
         views.ListCityStreets.as_view(),
         name='city-list'),
    path('city/',
         views.ListCities.as_view(),
         name='city-list'),
]
