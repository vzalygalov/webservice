from django.db import models

# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    street = models.ForeignKey('Street', on_delete=models.CASCADE)
    building_number = models.CharField(max_length=255)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return '{name}'.format(name=self.name)


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{name}'.format(name=self.name)


class Street(models.Model):
    name = models.CharField(max_length=255)
    city = models.ManyToManyField('City', related_name='streets')



