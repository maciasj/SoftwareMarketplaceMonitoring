from MonitoringSoftwareMarketplaces.models import *

def insertCategories(categories):
    count = 0
    for category in categories:
        category_obj = Category(
            identifier=count, 
            name=category['name'], 
            api_name=category['api_name'], 
            marketplace="microsoft",
            )
        count = count + 1
        print("Insertando categoria: ", category['name'] )
        category_obj.save()

def getCategories():
    categories = Category.objects.all()
    categories_list = []
    for category in categories:
        category_dict = {
            'name': category.name,
            'api_name': category.api_name,
            'marketplace': category.marketplace
        }
        categories_list.append(category_dict)
    return categories_list

def getCategoryAPI_name(category):
    category = Category.objects.get(name=category, marketplace="microsoft")
    return category.api_name

def searchProduct(query):
    try:
        products = Product.objects.filter(name__icontains=query, marketplace="microsoft")
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
    except Product.DoesNotExist:
        print("No se pudo encontrar el producto")
        return None

def insertProducts(products):
    productInserted = False
    for product in products:
        try:
            product_obj = Product(
            identifier=product['identifier'],
            name=product['name'],
            description=product['description'],
            type=product['type'],
            creator=product['creator'],
            api_name=product['api_name'],
            marketplace=product['marketplace'],
            url=product['url']
        )
            print("Insertando producto: ", product['name'])
            product_obj.save()
            productInserted = True
        except:
            print("No se pudo insertar el producto")
    if(not productInserted):
        return None
    return products


def getProductById(id):
    try: 
        product = Product.objects.get(identifier=id, marketplace="microsoft")
        product = {
        'identifier': product.identifier,
        'name': product.name,
        'description': product.description,
        'type': product.type,
        'creator': product.creator,
        'api_name': product.api_name,
        'marketplace': product.marketplace,
        'url': product.url}
        return product
    except Product.DoesNotExist:
        print("No existe el producto")
        return None

def deleteProduct(id):
    try:
        product = Product.objects.get(identifier=id, marketplace="microsoft")
        product.delete()
        return True
    except Product.DoesNotExist:
        print("No existe el producto")
        return None