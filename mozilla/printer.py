from django.http import HttpResponse
from .mozillaService import mozillaService

def bienvenidoEclispe(request):
    return HttpResponse("Bienvenido a Eclipse Marketplace")

def printCategories(request):
    return HttpResponse("Obteniendo todas las categorias y Marketplaces de Eclipse", mozillaService.getCategories(request))

def printProductsByMarketandCategory(request, category, market):
    response = EclipseService.getProductsByMarketplaceAndCategory(request,category, market)
    return HttpResponse(response.text)

def printProductByID(request, nodeId):
    return HttpResponse(EclipseService.getProductById(request, nodeId))

def printProductByTitle(request, title):
    return HttpResponse(EclipseService.getProductByTitle(request, title))

def printTopFavorites(request):
    return HttpResponse(EclipseService.getTopFavorites(request))