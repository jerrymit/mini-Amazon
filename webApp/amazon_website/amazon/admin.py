from django.contrib import admin
from .models import *
# Write the configuration file for the backend management system configuration.
# Register your models here.
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Shipment)
admin.site.register(Order)