from MonitoringSoftwareMarketplaces.models import *

MARKETPLACE = "eclipse"


def serializeProduct(product, categories, keywords):
    json_product ={
        'identifier': product.identifier,
        'url': product.url,
        'name': product.name,
        'categories': list(categories),
        'keywords': list(keywords),
        'description': product.description,
        'type': product.type,
        'creator': product.creator,
        'marketplace': MARKETPLACE,
       
    }
    return json_product

def insertCategories(categories):
    for category in categories:
        try:
            category_obj = Category(identifier=category['identifier'], name=category['name'], url=category['url'], marketplace=MARKETPLACE)
            print("Insertando categoria: ", category_obj)
            category_obj.save()
        except Exception as e:
            print("Error al insertar categoria: ", category['name'], e)

def insertMarkets(markets):
    for market in markets:
        try:
            market_obj = Market(identifier=market['identifier'], url=market['url'], name=market['name'], marketplace=MARKETPLACE)
            print("Insertando market: ", market['name'] )
            market_obj.save()
        except Exception as e:
            print("Error al insertar market: ", market['name'], e)

def insertCategoryInMarket(categories):
    print ("Insertando categorias en market")
    for category in categories:
        category_obj = Category.objects.get(identifier=category['identifier'])
        for market in category['market']:
            market_obj = Marketplace.objects.get(identifier=market, marketplace= MARKETPLACE)
            category_in_market = CategoryInMarket( category=category_obj, market=market_obj, marketplace=MARKETPLACE)
            category_in_market.save()
            print("Insertando categoria en market: ", category_in_market )
    
def insertSingleProduct(product):
    product_obj = Product(identifier=product['identifier'], 
                            url=product['url'],
                            name=product['name'], 
                            description=product['description'], 
                            type=product['type'], 
                            creator=product['creator'],
                            marketplace=MARKETPLACE)
    print("Insertando producto: ", product['name'])
    product_obj.save()

    #Insertar categorias en producto
    for category in product['categories']:
        category_in_product = CategoryInProduct(product=product['identifier'], category=category, marketplace=MARKETPLACE)
        if(not CategoryInProduct.objects.filter(product=product['identifier'], category=category).exists()):
            category_in_product.save()
            print("Insertando categoria en producto: ", category, "nombre  " , product['name'] )

    #Insertar tags en producto    
    for keywords in product['keywords']:
        keywords_in_product = ProductKeyword(product=product['identifier'], keywords=keywords, marketplace=MARKETPLACE)
        if(not ProductKeyword.objects.filter(product=product['identifier'], keywords=keywords).exists()):
            keywords_in_product.save()
            print("Insertando Tag en producto: ", keywords, "nombre  " , product['name'] )


        
def getMarkets():
    markets = Market.objects.filter(marketplace=MARKETPLACE)
    serialized_markets = []
    for market in markets:
        market = {
            'identifier': market.identifier,
            'url': market.url,
            'name': market.name,
            'marketplace': MARKETPLACE
        }
        serialized_markets.append(market)
    return serialized_markets



def getProductsByCategory(market, category):
    try:
        categoryName = Category.objects.get(identifier=category).name
    except Category.DoesNotExist:
        return 1
    try:
        productsIds = CategoryInProduct.objects.filter(category=categoryName).values_list('product', flat=True)
        json_products = []
        for product in list(productsIds):
            json_products.append(getProductById(product))
        return json_products
    except Product.DoesNotExist:    
        return 2

def getProductById(nodeId):
        product = Product.objects.get(identifier=nodeId, marketplace=MARKETPLACE)
        keywords = ProductKeyword.objects.filter(product=nodeId).values_list('keywords', flat=True)
        categories = CategoryInProduct.objects.filter(product=nodeId).values_list('category', flat=True)
        json_product = serializeProduct(product, categories, keywords)
        return json_product

def getProductsByQuery(query):
    products = Product.objects.filter(name__icontains=query, marketplace=MARKETPLACE)
    object_products = []
    for product in products:
        product = {
            'identifier': product.identifier,
            'name': product.name,
            'description': product.description,
            'type': product.type,
            'creator': product.creator,
            'marketplace': product.marketplace,
            'url': product.url
        }
        object_products.append(product)
    return object_products

def deleteProduct(id):
    try:
        product = Product.objects.get(identifier=id, marketplace=MARKETPLACE)
        product.delete()
        return 0
    except Product.DoesNotExist:
        return 1

def getKeywords():
    keywords = ProductKeyword.objects.filter(marketplace=MARKETPLACE).values_list('keywords').distinct()
    return list(keywords)

def getProductByKeyword(keyword):
    products = ProductKeyword.objects.filter(keywords=keyword, marketplace=MARKETPLACE).values_list('product', flat=True)
    print(products) 
    json_products = []
    for product in products:
        print(product)
        json_products.append(getProductById(product))
    return json_products