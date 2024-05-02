from django.http import HttpResponse
from .eclipseService import EclipseService

def bienvenidoEclispe(request):
    return HttpResponse("Bienvenido a Eclipse Marketplace")

def printCategories(request):
    return HttpResponse("Obteniendo todas las categorias y Marketplaces de Eclipse", EclipseService.getEclipseCategoriesAndMarketplaces(request))

def printProductsByMarketandCategory(request, category, market):
    response = EclipseService.getProductsByMarketplaceAndCategory(request,category, market)
    return HttpResponse(response.text)

def printproductByNodeID(request, nodeId):
    return HttpResponse(EclipseService.getProductById(request, nodeId))

def printProductByTitle(request, title):
    return HttpResponse(EclipseService.getProductByTitle(request, title))

def printTopFavorites(request):
    return HttpResponse(EclipseService.getTopFavorites(request))