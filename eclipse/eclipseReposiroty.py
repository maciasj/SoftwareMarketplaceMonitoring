from MonitoringSoftwareMarketplaces.models import *
import json
from django.forms.models import model_to_dict


def testUserInsert():
    dato_nuevo = Test(name='holafoo fhi ')
    dato_nuevo.save()

def getEclipse():
    return "eclipse"

def insertCategories(categories):

    for category in categories:
        print(category)
        category_obj = Category(id=category['id'], name=category['name'], url=category['url'], marketplace=getEclipse())
        print("Insertando categoria: ", category_obj)
        category_obj.save()

def insertMarkets(markets):
    for market in markets:
        market_obj = Market(id=market['id'], url=market['url'], name=market['name'], marketplace=getEclipse())
        print("Insertando market: ", market['name'] )
        market_obj.save()

def insertCategoryInMarket(categories):
    print ("Insertando categorias en market")
    for category in categories:
        category_obj = Category.objects.get(id=category['id'])
        for market in category['market']:
            market_obj = Marketplace.objects.get(id=market, marketplace= getEclipse())
            category_in_market = CategoryInMarket( category=category_obj, market=market_obj, marketplace=getEclipse())
            category_in_market.save()
            print("Insertando categoria en market: ", category_in_market )
    
def insertSingleProduct(product):
    product_obj = Product(id=product['id'], 
                            url=product['url'],
                            name=product['name'], 
                            description=product['description'], 
                            type=product['type'], 
                            autor=product['autor'],
                            api_name=product['api_name'], 
                            marketplace=getEclipse())
    print("Insertando producto: ", product_obj)
    product_obj.save()
    #Insertar categorias en producto
    for category in product['categories']:
        category_in_product = CategoryInProduct(product=product['id'], category=category, marketplace=getEclipse())
        if(not CategoryInProduct.objects.filter(product=product['id'], category=category).exists()):
            category_in_product.save()
            print("Insertando categoria en producto: ", category, "nombre  " , product['name'] )
    #Insertar tags en producto    
    for tag in product['tags']:
        tag_in_product = TagInProduct(product=product['id'], tag=tag, marketplace=getEclipse())
        if(not TagInProduct.objects.filter(product=product['id'], tag=tag).exists()):
            tag_in_product.save()
            print("Insertando Tag en producto: ", tag, "nombre  " , product['name'] )

def getCategories():
    return Category.objects.all()
def getMarkets():
    return Marketplace.objects.all()
def getProducts(market, category):
    categoryName = Category.objects.get(id=category).name
    productsIds = CategoryInProduct.objects.filter(category=categoryName).values_list('product', flat=True)
    json_products = []
    for product in list(productsIds):
        json_products.append(getProductById(product))
    return json_products

def getProductById(nodeId):
    product = Product.objects.get(id=nodeId)
    tags = TagInProduct.objects.filter(product=nodeId).values_list('tag', flat=True)
    categories = CategoryInProduct.objects.filter(product=nodeId).values_list('category', flat=True)
    json_product ={
        'id': product.id,
        'url': product.url,
        'name': product.name,
        'categories': list(categories),
        'tags': list(tags),
        'description': product.description,
        'type': product.type,
        'autor': product.autor,
        'api_name': product.api_name,
        'marketplace': product.marketplace,
       
        
    }
    return json_product