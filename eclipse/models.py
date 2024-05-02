# Create your models here.
from django.db import models

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    count = models.IntegerField()
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Marketplace(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.name