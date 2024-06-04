from MonitoringSoftwareMarketplaces.models import *

def getMozilla():
    return "mozilla"

def insertCategories(categories):
    for category in categories:
        print("Categoria: ", category)
        category_obj = Category(
            identifier=category['id'], 
            name=category['name'], 
            api_name=category['slug'], 
            marketplace="mozilla",
            description=category['description'],
            type=category['type'],)
        print("Insertando categoria: ", category['name'] )
        category_obj.save()

def insertKeywords(keywords):
    cont = 1
    parsed_keywords = []
    for keyword in keywords:
        keyword_obj = Keyword(identifier=cont, name=keyword, marketplace="mozilla")
        cont = cont + 1
        keyword_obj.save()
        parsed_keywords.append(keyword)
    return parsed_keywords


def getCategories():
    categories = Category.objects.filter(marketplace="mozilla")
    serialized_categories = []
    for category in categories:
        category = {
            'identifier': category.identifier,
            'name': category.name,
            'api_name': category.api_name,
            'url': category.url,
            'description': category.description,
            'marketplace': category.marketplace
        }
        serialized_categories.append(category)
    return serialized_categories

def getKeywords():
    keywords = Keyword.objects.filter(marketplace="mozilla").values('name')
    serialized_keywords = []
    for keyword in keywords:
        serialized_keywords.append(keyword['name'])
    return serialized_keywords

def getProductById(id):
    product = Product.objects.get(identifier=id, marketplace="mozilla")
    product = {
        'identifier': product.identifier,
        'name': product.name,
        'description': product.description,
        'type': product.type,
        'creator': product.creator,
        'api_name': product.api_name,
        'marketplace': product.marketplace,
        'url': product.url
    }
    return product

def existeCategory(category):
    category = Category.objects.filter(name=category)
    if category.exists():
        return True
    else:
        return False
    
def existeKewyword(keyword):
    keyword = Keyword.objects.filter(name=keyword)
    return keyword.exists()
    
def getProductByKewyword(Kewyword):
    keywordProduct = keywordsInProduct.objects.filter(keywords_icontains=Kewyword,marketplace="mozilla").values('product')
    object_products = []
    for element in keywordProduct:
        product = Product.objects.get(identifier=element['product'])
        product = {
            'identifier': product.identifier,
            'name': product.name,
            'description': product.description,
            'type': product.type,
            'creator': product.creator,
            'api_name': product.api_name,
            'marketplace': product.marketplace,
            'url': product.url
        }
        object_products.append(product)
    return object_products

def getProductByCategory(category):
    products = Product.objects.filter(category.contains(category))
    return products

def getCategoryInfo(category):
    newcategory = Category.objects.filter(name=category, marketplace="mozilla").values('name', 'api_name')
    objectCategory ={
        "category": newcategory[0]['name'],
        "api_name": newcategory[0]['api_name'],
    }
    return objectCategory

def insertSingleProduct(product):
    product_obj = Product(identifier=product['identifier'], 
                          url=product['url'],
                          name=product['name'], 
                          description=product['description'], 
                          type=product['type'], 
                          creator=product['creator'],
                          api_name=product['api_name'], 
                          marketplace=getMozilla())

    print("Insertando producto: ", product_obj.identifier)
    product_obj.description = product_obj.description.encode('utf-8')
    product_obj.save()
    #Insertar categorias en producto
    for category in product['categories']:
        category_in_product = CategoryInProduct(product=product['identifier'], category=category, marketplace=getMozilla())
        if(not CategoryInProduct.objects.filter(product=product['identifier'], category=category).exists()):
            category_in_product.save()
            print("Insertando categoria en producto: ", category)

    #Insertar tags en producto    
    for keywords in product['keywords']:
        keywords_in_product = keywordsInProduct(product=product['identifier'], keywords=keywords, marketplace=getMozilla())
        if(not keywordsInProduct.objects.filter(product=product['identifier'], keywords=keywords).exists()):
            keywords_in_product.save()
            print("Insertando Tag en producto: ", keywords)
    return product_obj


def getProductByQuery(query):
    products = Product.objects.filter(name__icontains=query, marketplace="mozilla")
    object_products = []
    for product in products:
        product = {
            'identifier': product.identifier,
            'name': product.name,
            'description': product.description,
            'type': product.type,
            'creator': product.creator,
            'api_name': product.api_name,
            'marketplace': product.marketplace,
            'url': product.url
        }
        object_products.append(product)
    return object_products
    
