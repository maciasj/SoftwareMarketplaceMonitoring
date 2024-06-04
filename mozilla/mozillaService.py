import os
import requests
import json
from django.http import JsonResponse
from . import mozillaRepository
from . import JSONMozillaParser
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
    
    def insertGroupProducts(products):
        newProducts = []
        for product in products:
            mozillaRepository.insertSingleProduct(product)
            newProducts.append(product)
        return newProducts
    
    def getCategories(request):
        #Obtenemos el valor de cache
        data = json.loads(request.body)
        cache = data.get('cache')
        if(cache):
            categories = mozillaRepository.getCategories()
            return JsonResponse(categories, safe=False,status=201)
        else:
            response = requests.get('https://addons.mozilla.org/api/v5/addons/categories/')
            if response.status_code == 200:
                mozillaRepository.insertCategories(response.json())
                return JsonResponse(response.json(), safe=False,status=202)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener las categorías"}, status=400)
    
    def getTags(request):
        data = json.loads(request.body)
        cache = data.get('cache')

        if(cache):
            Keywords = mozillaRepository.getKeywords()

            return JsonResponse(Keywords, safe=False,status=201)
        else:
            response = requests.get('https://addons.mozilla.org/api/v5/addons/tags/')
            print("Respuesta de Tags", response.text)
            data = response.json()
            if response.status_code == 200:
                tagsJson = mozillaRepository.insertKeywords(data)
                return JsonResponse(tagsJson, safe=False,status=201)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener los Tags "}, status=400)
    
    def getProductsByCategory(request):
        #Obtenemos el valor de los parametros enviados
        data = json.loads(request.body)
        cache = data.get('cache')
        category = data.get('category')
        type = data.get('type')
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
            response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?category={}&type={}'.format(categoryInfo["api_name"],type))
            if response.status_code == 200:
                products = response.json()
                insertProducts = JSONMozillaParser.JSONMozillaParser.parseProducts(products)
                newProducts = mozillaService.insertGroupProducts(insertProducts)
                return JsonResponse(newProducts, safe=False,status=202)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener las categorías"}, response.status_code)
    
    def getProductsByKewyword(request):
        #Obtenemos el valor de los parametros enviados
        data = json.loads(request.body)
        cache = data.get('cache')
        keyword = data.get('keyword')
        #Comprobamos si la categoria existe
        #if(not mozillaRepository.existeKewyword(keyword)):
         #       return JsonResponse({"error": "La categoria introducida no existe"}, status=500)
        #Si se nos indica que se debe de usar cache se obtiene la informacion de la base de datos
        if(cache):
            pruduct = mozillaRepository.getProductByKewyword(keyword)
            return JsonResponse(pruduct, safe=False,status=201)
        #si no se nos indica que se debe de usar cache se obtiene la informacion de la api
        else:
            response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?tag='+keyword)
            if response.status_code == 200:
                insertProducts = JSONMozillaParser.JSONMozillaParser.parseProducts(response.json())
                print("PRODUCTOS", insertProducts)
                newProducts = mozillaService.insertGroupProducts(insertProducts)
                return JsonResponse(newProducts, safe=False,status=202)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener las categorías"}, response.status_code)

    def getProductById(request, productId):
        data = json.loads(request.body)
        cache = data.get('cache')
        if(cache):
            product = mozillaRepository.getProductById(productId)
            print("Producto",product)
            if(product):
                return JsonResponse(product, safe=False,status=201)
            else:
                return JsonResponse({"error": "No se pudo encontrar el producto"}, status=400)
        else:
            print("productId",productId)
            response = requests.get('https://addons.mozilla.org/api/v5/addons/addon/'+productId)
            if response.status_code == 200:
                parsedProduct = JSONMozillaParser.JSONMozillaParser.parseInfoSingleProduct(response.json())
                mozillaRepository.insertSingleProduct(parsedProduct)
                return JsonResponse(parsedProduct, safe=False,status=202)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener el producto"}, response.status_code)
    
    def getProductByQuery(request):
        data = json.loads(request.body)
        cache = data.get('cache')
        query = data.get('query')
        if(cache):
            products = mozillaRepository.getProductByQuery(query)
            if(products):
                return JsonResponse(products, safe=False,status=201)
            else:
                return JsonResponse({"error": "No se pudo obtener ningun producto para esta query"}, status=400)
        response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?q ='+query)
        if (response.status_code == 200):
                insertProducts = JSONMozillaParser.JSONMozillaParser.parseProducts(response.json())
                newProducts = mozillaService.insertGroupProducts(insertProducts)
                return JsonResponse(newProducts, safe=False,status=202)
        else:
        # En caso de error, devolver un mensaje de error
            return JsonResponse({"error": "No se pudo obtener el producto"}, status=400)
    
    def discoveryProdcuts(request):
        response = requests.get('https://addons.mozilla.org/api/v5/discovery')
        if response.status_code == 200:
            products = response.json()
            productGUIDs = JSONMozillaParser.JSONMozillaParser.parseGUIDs(products)
            response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?guid='+productGUIDs)
            if response.status_code == 200:
                insertProducts = JSONMozillaParser.JSONMozillaParser.parseProducts(response.json())
                newProducts = mozillaService.insertGroupProducts(insertProducts)
                return JsonResponse(newProducts, safe=False,status=202)
        else:
        # En caso de error, devolver un mensaje de error
            return JsonResponse({"error": "Error en la llamada"}, response.status_code)