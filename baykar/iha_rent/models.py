from django.db import models
from django.contrib.auth.hashers import make_password

class Users(models.Model):
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

class IhaDetails(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    height = models.FloatField(default=0)
    category = models.CharField(max_length=100)

class RentRecords(models.Model):
    user_id = models.BigIntegerField(default=0)
    iha_id = models.BigIntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


