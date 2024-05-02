from django.http import HttpResponse
from .mozillaController import mozillaController

def bienvenidoEclispe(request):
    return HttpResponse("Bienvenido a Eclipse Marketplace")

def printCategories(request):
    return HttpResponse("Obteniendo todas las categorias y Marketplaces de Eclipse", mozillaController.getCategories(request))

def printProductsByMarketandCategory(request, category, market):
    response = mozillaController.getProductsByMarketplaceAndCategory(request,category, market)
    return HttpResponse(response.text)

def printProductByID(request, nodeId):
    return HttpResponse(mozillaController.getProductById(request, nodeId))

def printProductByTitle(request, title):
    return HttpResponse(mozillaController.getProductByTitle(request, title))

def printTopFavorites(request):
    return HttpResponse(mozillaController.getTopFavorites(request))