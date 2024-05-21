from MonitoringSoftwareMarketplaces.models import *


def insertCategories(categories):
    for category in categories:
        category_obj = Category(id=category['id'], name=category['name'], slug=category['slug'], type=category['type'], description=category['description'])
        print("Insertando categoria: ", category['name'] )
        category_obj.save()
def insertProduct(product):
    product_obj = Product(id=product['guid'], name=product['name'], slug=product['slug']  )
    print("Insertando producto: ", product['name'])
    product_obj.save()

def getCategories():
    categories = Category.objects.values_list('name')
    print("Devolviendo categorias: ", categories)
    return categories

def getTags():
    tags = Tag.objects.values_list('name')
    return tags

def getProductById(id):
    product = Product.objects.get(id=id)
    return product

def existeCategory(category):
    category = Category.objects.filter(name=category)
    if category.exists():
        return True
    else:
        return False
    
def existeTag(tag):
    tag = Tag.objects.filter(name=tag)
    if tag.exists():
        return True
    else:
        return False
def getProductByTag(tag):
    products = Product.objects.filter(tag.contains(tag))
    return products

def getProductByCategory(category):
    products = Product.objects.filter(category.contains(category))
    return products

def getCategoryInfo(category):
    category = Category.objects.get(name=category)
    return category