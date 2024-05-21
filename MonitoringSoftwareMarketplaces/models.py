from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    rating = models.FloatField()
    conmpanyName = models.CharField(max_length=100)
    price = models.FloatField()
    tags = models.ManyToManyField('Tag')
    categories = models.ManyToManyField('Category')
    type = models.CharField(max_length=100)
    marketPlace = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Market(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Type(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name