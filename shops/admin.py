from django.contrib import admin
from .models import City, Street, Shop

# Register your models here.


class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class StreetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(City, CityAdmin)
admin.site.register(Street, StreetAdmin)
