import os
import requests
import json
from django.http import JsonResponse
from . import microsoftParser
from MonitoringSoftwareMarketplaces.serviceInterface import serviceInterface
from MonitoringSoftwareMarketplaces.repository import Repository

MARKETPLACE = "microsoft"   
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
        Repository.insertCategoriesMS(categories)
        return JsonResponse( categories ,safe=False,status=201)
    
    def getCategories(request):
        categories = Repository.getCategories(MARKETPLACE)
        return JsonResponse(categories,safe=False,status=200)
    
    def getProductByQuery(request):
        cache = request.GET.get('cache')
        query = request.GET.get('query')
        match = request.GET.get('match')
        if(cache=="1"):
            pruducts = Repository.getProductsByQuery(query,MARKETPLACE)
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
                    Repository.insertGroupProducts(products, MARKETPLACE)
                    return JsonResponse(products, safe=False,status=200)
                else:
                    return JsonResponse({"error": "No se pudo obtener los productos"}, response.status_code)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener los productos"}, response.status_code)
    
    def getProductById(request, id):
        cache = request.GET.get('cache')
        if(cache=="1"):
            product = Repository.getProductById(id, MARKETPLACE)
            if product is None:
                return JsonResponse({"error": "No se pudo encontrar el producto"}, status=404)
            return JsonResponse(product, safe=False,status=200)
        else:
            params = {
                'productIds': id,
            }
            response = requests.post('https://storeedgefd.dsx.mp.microsoft.com/v8.0/sdk/products?market=US&locale=en-US&deviceFamily=Windows.Desktop',json=params)
            if response.status_code == 200:
                product = microsoftParser.microsoftParser.parseProducts(response.json())
                print(product)
                Repository.insertGroupProducts(product, MARKETPLACE)
                return JsonResponse(product, safe=False,status=200)
            else:
                return JsonResponse({"error": "No se pudo obtener el producto"}, response.status_code)
            
    def addProduct(request):
        data = json.loads(request.body)
        products = Repository.insertGroupProducts(data,MARKETPLACE)
        if products is None:
            return JsonResponse({"error": "No se pudo insertar el producto"}, status=404)
        return JsonResponse( {"message": "Productos añadidos correctamente"} ,safe=False,status=201)
    
    def deleteProduct(request, id):
        product = Repository.deleteProduct(id, MARKETPLACE)
        if product is None:
            return JsonResponse({"message": "Producto no encontrado"}, status=204)
        return JsonResponse( {"message": "Producto eliminado correctamente"}, status=202)
    