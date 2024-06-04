from MonitoringSoftwareMarketplaces.models import *



def testUserInsert():
    dato_nuevo = Test(name='holafoo fhi ')
    dato_nuevo.save()

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
        'api_name': product.api_name,
        'marketplace': product.marketplace,
       
    }
    return json_product
def getEclipse():
    return "eclipse"

def insertCategories(categories):

    for category in categories:
        print(category)
        category_obj = Category(identifier=category['identifier'], name=category['name'], url=category['url'], marketplace=getEclipse())
        print("Insertando categoria: ", category_obj)
        category_obj.save()

def insertMarkets(markets):
    for market in markets:
        market_obj = Market(identifier=market['identifier'], url=market['url'], name=market['name'], marketplace=getEclipse())
        print("Insertando market: ", market['name'] )
        market_obj.save()

def insertCategoryInMarket(categories):
    print ("Insertando categorias en market")
    for category in categories:
        category_obj = Category.objects.get(identifier=category['identifier'])
        for market in category['market']:
            market_obj = Marketplace.objects.get(identifier=market, marketplace= getEclipse())
            category_in_market = CategoryInMarket( category=category_obj, market=market_obj, marketplace=getEclipse())
            category_in_market.save()
            print("Insertando categoria en market: ", category_in_market )
    
def insertSingleProduct(product):
    product_obj = Product(identifier=product['identifier'], 
                            url=product['url'],
                            name=product['name'], 
                            description=product['description'], 
                            type=product['type'], 
                            creator=product['creator'],
                            api_name=product['api_name'], 
                            marketplace=getEclipse())
    print("Insertando producto: ", product_obj)
    product_obj.save()
    #Insertar categorias en producto
    for category in product['categories']:
        category_in_product = CategoryInProduct(product=product['identifier'], category=category, marketplace=getEclipse())
        if(not CategoryInProduct.objects.filter(product=product['identifier'], category=category).exists()):
            category_in_product.save()
            print("Insertando categoria en producto: ", category, "nombre  " , product['name'] )
    #Insertar tags en producto    
    for keywords in product['keywords']:
        keywords_in_product = keywordsInProduct(product=product['identifier'], keywords=keywords, marketplace=getEclipse())
        if(not keywordsInProduct.objects.filter(product=product['identifier'], keywords=keywords).exists()):
            keywords_in_product.save()
            print("Insertando Tag en producto: ", keywords, "nombre  " , product['name'] )

def getCategories():
    categories = Category.objects.filter(marketplace="eclipse")
    serialized_categories = []
    for category in categories:
        category = {
            'identifier': category.identifier,
            'name': category.name,
            'url': category.url,
            'marketplace': category.marketplace
        }
        serialized_categories.append(category)
    return serialized_categories
        
def getMarkets():
    markets = Market.objects.all()
    serialized_markets = []
    for market in markets:
        market = {
            'identifier': market.identifier,
            'url': market.url,
            'name': market.name,
            'marketplace': market.marketplace
        }
        serialized_markets.append(market)
    return serialized_markets



def getProducts(market, category):
    categoryName = Category.objects.get(identifier=category).name
    productsIds = CategoryInProduct.objects.filter(category=categoryName).values_list('product', flat=True)
    json_products = []
    for product in list(productsIds):
        json_products.append(getProductById(product))
    return json_products

def getProductById(nodeId):
    product = Product.objects.get(identifier=nodeId)
    keywords = keywordsInProduct.objects.filter(product=nodeId).values_list('keywords', flat=True)
    categories = CategoryInProduct.objects.filter(product=nodeId).values_list('category', flat=True)
    json_product = serializeProduct(product, categories, keywords)
    return json_product

def getProductsByQuery(query):
    products = Product.objects.filter(name__contains=query)
    json_products = []
    for product in products:
        keywords = keywordsInProduct.objects.filter(product=product.identifier).values_list('keywords', flat=True)
        categories = CategoryInProduct.objects.filter(product=product.identifier).values_list('category', flat=True)
        json_product = serializeProduct(product, categories, keywords)
        json_products.append(json_product)
    return json_products