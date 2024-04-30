from django.http import HttpResponse
from .eclipseService import getEclipseCategoriesAndMarketplaces,getProductsByMarketplaceAndCategory,getProductById,getProductByTitle,getTopFavorites

def bienvenidoEclispe(request):
    return HttpResponse("Bienvenido a Eclipse Marketplace")

def printCategories(request):
    return HttpResponse("Obteniendo todas las categorias y Marketplaces de Eclipse", getEclipseCategoriesAndMarketplaces(request))

def printProductsByMarketandCategory(request, category, market):
    response = getProductsByMarketplaceAndCategory(request,category, market)
    return HttpResponse(response.text)

def printproductByNodeID(request, nodeId):
    return HttpResponse(getProductById(request, nodeId))

def printProductByTitle(request, title):
    return HttpResponse(getProductByTitle(request, title))

def printTopFavorites(request):
    return HttpResponse(getTopFavorites(request))