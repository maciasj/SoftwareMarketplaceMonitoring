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

def insertProducts(products):
    for product in products:
        product_obj = Product(id=product['id'], 
                              url=product['url'], 
                              name=product['name'], 
                              short_description=product['shortdescription'])
        for category in product['categories']:
            category_obj = Category.objects.get(id=category)
            product_obj.categories.add(category_obj)
        product_obj.save()
        print("Insertando producto: ", product['name'] )
