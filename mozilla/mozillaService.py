import os
import requests
import json
from django.http import JsonResponse
from . import mozillaRepository
from MonitoringSoftwareMarketplaces.serviceInterface import serviceInterface

class mozillaService(serviceInterface):
    
    def test(request):
        data = json.loads(request.body)
        cache = data.get('cache')
        category = data.get('category')
        for cat in category:
            print("Categoria", cat)
        if(cache): 
            print("cache", cache)
        else:
            print("no cache")
        return JsonResponse(cache,safe=False,status=201)
    
    def getCategories(request):
        #Obtenemos el valor de cache
        data = json.loads(request.body)
        cache = data.get('cache')

        if(cache == 'true'):
            categories = mozillaRepository.getCategories()
            return JsonResponse(categories, safe=False,status=201)
        else:
            response = requests.get('https://addons.mozilla.org/api/v5/addons/categories/')
            print("RESpuesta de categorias text", response.text)
            if response.status_code == 200:
                mozillaRepository.insertCategories(response.json())
                categorias = response.json()
                return JsonResponse(categorias, safe=False,status=202)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener las categorías"}, status=400)
    
    def getTags(request):
        data = json.loads(request.body)
        cache = data.get('cache')

        if(cache == 'true'):
            tags = mozillaRepository.getTags(id)
            return JsonResponse(tags, safe=False,status=201)
        else:
            response = requests.get('https://addons.mozilla.org/api/v5/addons/tags/')
            print("RESpuesta de Tags", response.text)
            if response.status_code == 200:
                tags = response.json()
                return JsonResponse(tags, safe=False,status=201)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener los Tags "}, status=400)
    
    def getProductsByCategory(request):
        #Obtenemos el valor de los parametros enviados
        data = json.loads(request.body)
        cache = data.get('cache')
        category = data.get('category')
        #Comprobamos si la categoria existe
        if(not mozillaRepository.existeCategory(category)):
                return JsonResponse({"error": "La categoria introducida no existe"}, status=500)
        #Si se nos indica que se debe de usar cache se obtiene la informacion de la base de datos
        if(cache):
            pruduct = mozillaRepository.getProductByCategory(category)
            return JsonResponse(pruduct, safe=False,status=201)
        #si no se nos indica que se debe de usar cache se obtiene la informacion de la api
        else:
            categoryInfo = mozillaRepository.getCategoryInfo(category)
            response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?category='+categoryInfo["slug"]+"&type="+categoryInfo['type'])
            if response.status_code == 200:
                products = response.json()
                return JsonResponse(products, safe=False,status=202)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener las categorías"}, response.status_code)
    
    def getProductsByTag(request):
        #Obtenemos el valor de los parametros enviados
        data = json.loads(request.body)
        cache = data.get('cache')
        tag = data.get('tag')
        #Comprobamos si la categoria existe
        if(not mozillaRepository.existeTag(tag)):
                return JsonResponse({"error": "La categoria introducida no existe"}, status=500)
        #Si se nos indica que se debe de usar cache se obtiene la informacion de la base de datos
        if(cache):
            pruduct = mozillaRepository.getProductByTag(tag)
            return JsonResponse(pruduct, safe=False,status=201)
        #si no se nos indica que se debe de usar cache se obtiene la informacion de la api
        else:
            categoryInfo = mozillaRepository.getCategoryInfo(tag)
            response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?tag='+categoryInfo["slug"]+"&type="+categoryInfo['type'])
            if response.status_code == 200:
                products = response.json()
                return JsonResponse(products, safe=False,status=201)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener las categorías"}, response.status_code)

    def getProductById(request, productId):
        data = json.loads(request.body)
        cache = data.get('cache')
        if(cache):
            pruduct = mozillaRepository.getProductById(productId)
            if(product):
                return JsonResponse(pruduct, safe=False,status=201)
            else:
                return JsonResponse({"error": "No se pudo obtener el producto"}, status=400)
        else:
            print("productId",productId)
            response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?guid='+productId)
            if response.status_code == 200:
                #mozillaRepository.insertProduct(response.json())
                product = response.json()
                return JsonResponse(product, safe=False,status=202)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener el producto"}, response.status_code)
    
    def getProductByTitle(request, name):
        data = json.loads(request.body)
        cache = data.get('cache')
        if(cache):
            pruduct = mozillaRepository.getProductById(name)
            if(product):
                return JsonResponse(pruduct, safe=False,status=201)
            else:
                return JsonResponse({"error": "No se pudo obtener el producto, asegúrate de escribir bien el id"}, status=400)
        else:
            
            response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?guid='+name)
            if response.status_code == 200:
                #mozillaRepository.insertProduct(response.json())
                product = response.json()
                return JsonResponse(product, safe=False,status=202)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener el producto"}, status=400)
   
    def getProductByQuery(request):
        data = json.loads(request.body)
        cache = data.get('cache')
        query = data.get('query')
        response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?q ='+query)
        if response.status_code == 200:
            #mozillaRepository.insertProduct(response.json())
            products = response.json()
            return JsonResponse(products, safe=False,status=202)
        else:
        # En caso de error, devolver un mensaje de error
            return JsonResponse({"error": "No se pudo obtener el producto"}, status=400)
    
    def discoveryProdcuts(request):
        response = requests.get('https://addons.mozilla.org/api/v5/discovery')
        if response.status_code == 200:
            #mozillaRepository.insertProduct(response.json())
            products = response.json()
            return JsonResponse(products, safe=False,status=202)
        else:
        # En caso de error, devolver un mensaje de error
            return JsonResponse({"error": "Error en la llamada"}, response.status_code)