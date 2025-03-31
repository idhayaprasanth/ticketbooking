from django.contrib import admin
from busapp.models import create_bus,Payment

# Register your models here.
admin.site.register(create_bus)
admin.site.register(Payment)
class create_bus(admin.ModelAdmin):
    bus_details=['disno','routeno','busroute','bustype','image','bustime','busstops','stop1','stop2','stop3','stop4','stop5']
