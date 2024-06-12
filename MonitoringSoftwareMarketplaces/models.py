# Create your models here.
from django.db import models


    
class Category(models.Model):
    identifier = models.IntegerField(primary_key=True)
    name = models.TextField()
    api_name = models.TextField()
    url = models.URLField(max_length=200)
    description = models.TextField()
    marketplace = models.TextField()
    type = models.TextField()
    class Meta:
        db_table = 'Category'
    def __str__(self):
        return self.name
    
class CategoryInProduct(models.Model):
    product = models.IntegerField()
    category = models.TextField()
    marketplace = models.TextField()
    class Meta:
        db_table = 'CategoryInProduct'
    def __str__(self):
        return self.name
        
class Marketplace(models.Model):
    name = models.TextField(primary_key=True)
    class Meta:
        db_table = 'Marketplace'
    def __str__(self):
        return self.name    

class Market(models.Model):
    identifier = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=200)
    name = models.TextField()
    marketplace = models.TextField()
    class Meta:
        db_table = 'Market'
    def __str__(self):
        return self.name

class CategoryInMarket(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    marketplace = models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'CategoryInMarket'
    
class Keyword(models.Model):
    identifier = models.IntegerField(primary_key=True)
    name = models.TextField()
    marketplace = models.TextField()
    class Meta:
        db_table = 'Keywords'
    def __str__(self):
        return self.name
    
class Product(models.Model):
    identifier = models.CharField(primary_key=True, max_length=150)
    url = models.URLField(max_length=200)
    name = models.TextField()
    description = models.TextField()
    type = models.TextField()
    creator = models.TextField()
    api_name = models.TextField()
    marketplace = models.TextField()
    class Meta:
        db_table = 'Product'
    def __str__(self):
        return self.name


class ProductKeyword(models.Model):
    product = models.IntegerField()
    keywords = models.TextField()
    marketplace = models.TextField()
    class Meta:
        db_table = 'ProductKeyword'
    def __str__(self):
        return self.name    
    
class Test(models.Model):
    name = models.CharField(max_length=100)


def __str__(self):
    return self.name