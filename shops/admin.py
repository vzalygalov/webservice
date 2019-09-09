from django.contrib import admin
from .models import City, Street, Shop

# Register your models here.


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_streets')
    search_fields = ('name', 'streets__name')

    def get_streets(self, obj):
        return ', '.join([street.name for street in obj.streets.all()])


class StreetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('city',)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'street', 'building_number')
    search_fields = ('name', 'city__name', 'street__name')


admin.site.register(City, CityAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(Shop, ShopAdmin)
