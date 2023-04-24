from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import random
# Files that interact with the database. PostgreSQL
# Create your models here.



class Product(models.Model):
    description = models.TextField()
    count = models.IntegerField()

class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    location_x = models.IntegerField()
    location_y = models.IntegerField()
    
class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key = True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    destination_x = models.IntegerField()
    destination_y = models.IntegerField()
    status = models.CharField(max_length = 200, null=True, default="ordering")
    create_time = models.DateTimeField(default=timezone.now)
    truck_id = models.IntegerField(null=True)

class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null=True)
    quantity = models.IntegerField()
    order_time = models.DateTimeField(default=timezone.now)
    shipment = models.ForeignKey(Shipment, on_delete = models.CASCADE)

class Cart(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

'''
class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    destination_x = models.IntegerField()
    destination_y = models.IntegerField()
    status = models.CharField(max_length=20)  # packing, packed, loading, loaded, delivering, delivered

class Package(models.Model):
    package_id = models.AutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
'''