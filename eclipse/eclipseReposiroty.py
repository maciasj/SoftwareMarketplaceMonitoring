from .models import *

def testUserInsert():
    dato_nuevo = Test(name='holafoo fhi ')
    dato_nuevo.save()

def insertCategories(categories):
    for category in categories:
        category_obj = Category(id=category['id'], count=category['count'], url=category['url'], name=category['name'])
        print("Insertando categoria: ", category['name'] )
        category_obj.save()

def insertMarkets(markets):
    for market in markets:
        market_obj = Marketplace(id=market['id'], url=market['url'], name=market['name'])
        print("Insertando market: ", market['name'] )
        market_obj.save()