from django.http import HttpResponse
from .eclipseController import EclipseController

def bienvenidoEclispe(request):
    return HttpResponse("Bienvenido a Eclipse Marketplace")

def printCategories(request):
    return HttpResponse("Obteniendo todas las categorias y Marketplaces de Eclipse", EclipseController.getEclipseCategoriesAndMarketplaces(request))

def printProductsByMarketandCategory(request, category, market):
    response = EclipseController.getProductsByMarketplaceAndCategory(request,category, market)
    return HttpResponse(response.text)

def printproductByNodeID(request, nodeId):
    return HttpResponse(EclipseController.getProductById(request, nodeId))

def printProductByTitle(request, title):
    return HttpResponse(EclipseController.getProductByTitle(request, title))

def printTopFavorites(request):
    return HttpResponse(EclipseController.getTopFavorites(request))