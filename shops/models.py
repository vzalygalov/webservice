from django.db import models

# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    street = models.ForeignKey('Street', on_delete=models.CASCADE)
    building_number = models.CharField(max_length=255)
    time_to_open = models.TimeField()
    time_to_close = models.TimeField()


class City(models.Model):
    name = models.CharField(max_length=255)


class Street(models.Model):
    name = models.CharField(max_length=255)
    city = models.ManyToManyField('City')



