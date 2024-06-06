import os
import requests
import json
from django.http import JsonResponse
from . import microsoftRepository
from . import microsoftParser
from MonitoringSoftwareMarketplaces.serviceInterface import serviceInterface

class microsoftService(serviceInterface):
    
    def getSearchURL(filters,categoryAPIname):
        url = 'https://apps.microsoft.com/search?query='+filters['query']+'&department=Apps'
        if(filters['category']):
            url = url + '&category=' + categoryAPIname
        if(filters['type']):
            url = url + '&price=' + filters['type']
        return url
    
    def addCategories(request):
        data = json.loads(request.body)
        categories = data.get('categories')
        microsoftRepository.insertCategories(categories)
        return JsonResponse( categories ,safe=False,status=201)
    
    def getCategories(request):
        categories = microsoftRepository.getCategories()
        return JsonResponse(categories,safe=False,status=200)
    
    def searchProduct(request):
        cache = request.GET.get('cache')
        query = request.GET.get('query')
        match = request.GET.get('match')
        if(cache=="0"):
            pruducts = microsoftRepository.searchProduct(query)
            if pruducts is None:
                return JsonResponse({"error": "No se pudo encontrar el producto"}, status=404)
            return JsonResponse(pruducts, safe=False,status=200)
        else:
            parameters = {'Query': {
                'KeyWord': query,
                'MatchType': match
            }}
            response = requests.post('https://storeedgefd.dsx.mp.microsoft.com/v9.0/manifestSearch',json=parameters)
            if response.status_code == 200:
                productids = microsoftParser.microsoftParser.getIds(response.json())
                secondResponse = requests.post('https://storeedgefd.dsx.mp.microsoft.com/v8.0/sdk/products?market=US&locale=en-US&deviceFamily=Windows.Desktop',json=productids)
                if response.status_code == 200:
                    products = microsoftParser.microsoftParser.parseProducts(secondResponse.json())
                    microsoftRepository.insertProducts(products)
                    return JsonResponse(products, safe=False,status=201)
                else:
                    return JsonResponse({"error": "No se pudo obtener los productos"}, response.status_code)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener las categorías"}, response.status_code)
    
    def getProductById(request, id):
        cache = request.GET.get('cache')
        if(cache=="0"):
            product = microsoftRepository.getProductById(id)
            if product is None:
                return JsonResponse({"error": "No se pudo encontrar el producto"}, status=404)
            return JsonResponse(product, safe=False,status=201)
        else:
            params = {
                'productIds': id,
            }
            response = requests.post('https://storeedgefd.dsx.mp.microsoft.com/v8.0/sdk/products?market=US&locale=en-US&deviceFamily=Windows.Desktop',json=params)
            if response.status_code == 200:
                product = microsoftParser.microsoftParser.parseProducts(response.json())
                microsoftRepository.insertProducts(product)
                return JsonResponse(product, safe=False,status=202)
            else:
                return JsonResponse({"error": "No se pudo obtener el producto"}, response.status_code)
            

    def addProduct(request):
        data = json.loads(request.body)
        products = microsoftRepository.insertProducts(data)
        if products is None:
            return JsonResponse({"error": "No se pudo insertar el producto"}, status=404)
        return JsonResponse( {"message": "Productos añadidos correctamente"} ,safe=False,status=201)
    
    def deleteProduct(request, id):
        product = microsoftRepository.deleteProduct(id)
        if product is None:
            return JsonResponse({"message": "Producto no encontrado"}, status=204)
        return JsonResponse( {"message": "Producto eliminado correctamente"}, status=202)
    