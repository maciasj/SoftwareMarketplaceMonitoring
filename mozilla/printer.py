from django.http import HttpResponse
from .mozillaController import mozillaController

def printCategories(request):
    return HttpResponse("Obteniendo todas las categorias de Mozilla", mozillaController.getCategories(request))

def printCategories(request):
    return HttpResponse("Obteniendo todas las etiqueras de Mozilla", mozillaController.getTags(request))

def printByCategory(request, category, market):
    response = mozillaController.getProductsByMarketplaceAndCategory(request,category, market)
    return HttpResponse(response.text)

def printProductByID(request, nodeId):
    return HttpResponse(mozillaController.getProductById(request, nodeId))

def printProductByTitle(request, title):
    return HttpResponse(mozillaController.getProductByTitle(request, title))

def printTopFavorites(request):
    return HttpResponse(mozillaController.getTopFavorites(request))