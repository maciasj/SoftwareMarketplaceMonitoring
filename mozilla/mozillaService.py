import os
import requests
import json
from django.http import JsonResponse
from . import mozillaRepository
from . import JSONMozillaParser
from MonitoringSoftwareMarketplaces.serviceInterface import serviceInterface

class mozillaService(serviceInterface):
    
  
    def insertGroupProducts(products):
        newProducts = []
        for product in products:
            mozillaRepository.insertSingleProduct(product)
            newProducts.append(product)
        return newProducts
    
    def getCategories(request):
        cache = request.GET.get('cache')
        if(cache == "1"):
            try:
                categories = mozillaRepository.getCategories()
                return JsonResponse(categories, safe=False,status=201)
            except:
                return JsonResponse({"error": "No se pudo obtener las categorías"}, status=400)
        else:
            try:
                response = requests.get('https://addons.mozilla.org/api/v5/addons/categories/')
                if response.status_code == 200:
                    mozillaRepository.insertCategories(response.json())
                    return JsonResponse(response.json(), safe=False,status=202)
                else:
                # En caso de error, devolver un mensaje de error
                    return JsonResponse({"error": "No se pudo obtener las categorías"}, status=400)
            except:
                return JsonResponse({"error": "No se pudo obtener las categorías"}, status=400)
            
    def getKeywords(request):
        cache = request.GET.get('cache')
        if(cache == "1"):
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
        cache = request.GET.get('cache')
        category = request.GET.get('category')
        type = request.GET.get('type')

        #Comprobamos si la categoria existe
        if(not mozillaRepository.existeCategory(category)):
                return JsonResponse({"error": "La categoria introducida no existe"}, status=500)
        #Si se nos indica que se debe de usar cache se obtiene la informacion de la base de datos
        if(cache == "1"):
            try: 
                pruduct = mozillaRepository.getProductByCategory(category)
                return JsonResponse(pruduct, safe=False,status=201)
            except:
                return JsonResponse({"error": "No se pudo obtener los productos"}, status=500)
        #si no se nos indica que se debe de usar cache se obtiene la informacion de la api
        else:
            try:    
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
            except:
                return JsonResponse({"error": "No se pudo obtener las categorías"}, status=500)
    
    def getProductsByKewyword(request):
        #Obtenemos el valor de los parametros enviados
        cache = request.GET.get('cache')
        keyword = request.GET.get('keyword')
        if(not mozillaRepository.existeKewyword(keyword)):
            return JsonResponse({"error": "La categoria introducida no existe"}, status=500)
        if(cache == "1"):
            try:
             pruduct = mozillaRepository.getProductByKewyword(keyword)
             return JsonResponse(pruduct, safe=False,status=201)
            except:
                return JsonResponse({"error": "No se pudo obtener los productos"}, status=500)
        #si no se nos indica que se debe de usar cache se obtiene la informacion de la api
        else:
            response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?tag='+keyword)
            if response.status_code == 200:
                try:
                    insertProducts = JSONMozillaParser.JSONMozillaParser.parseProducts(response.json())
                    print("PRODUCTOS", insertProducts)
                    newProducts = mozillaService.insertGroupProducts(insertProducts)
                    return JsonResponse(newProducts, safe=False,status=202)
                except:
                    return JsonResponse({"error": "Ha habido un problema al obtener los productos"}, status=500)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener las categorías"}, response.status_code)

    def getProductById(request, productId):
        cache = request.GET.get('cache')
        if(cache == "1"):
            product = mozillaRepository.getProductById(productId)
            print("Producto",product)
            if(product):
                return JsonResponse(product, safe=False,status=201)
            else:
                return JsonResponse({"error": "No se pudo encontrar el producto"}, status=400)
        else:
            try:    
                print("productId",productId)
                response = requests.get('https://addons.mozilla.org/api/v5/addons/addon/'+productId)
                if response.status_code == 200:
                    parsedProduct = JSONMozillaParser.JSONMozillaParser.parseInfoSingleProduct(response.json())
                    mozillaRepository.insertSingleProduct(parsedProduct)
                    return JsonResponse(parsedProduct, safe=False,status=202)
                else:
                # En caso de error, devolver un mensaje de error
                    return JsonResponse({"error": "No se pudo obtener el producto"}, response.status_code)
            except:   
                return JsonResponse({"error": "No se pudo obtener el producto"}, status=400)
    
    def getProductByQuery(request):
        cache = request.GET.get('cache')
        query = request.GET.get('query')

        if(cache == "1"):
            try:
                products = mozillaRepository.getProductByQuery(query)
                if(products):
                    return JsonResponse(products, safe=False,status=201)
                else:
                    return JsonResponse({"error": "No se pudo obtener ningun producto para esta query"}, status=400)
            except:
                return JsonResponse({"error": "No se pudo obtener los productos"}, status=500)
        response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?q ='+query)
        if (response.status_code == 200):
                try:
                    insertProducts = JSONMozillaParser.JSONMozillaParser.parseProducts(response.json())
                    newProducts = mozillaService.insertGroupProducts(insertProducts)
                    return JsonResponse(newProducts, safe=False,status=202)
                except:
                    return JsonResponse({"error": "No se pudo obtener el producto"}, status=400)
        else:
        # En caso de error, devolver un mensaje de error
            return JsonResponse({"error": "No se pudo obtener el producto"}, status=400)
    
    def discoveryProdcuts(request):
        response = requests.get('https://addons.mozilla.org/api/v5/discovery')
        if response.status_code == 200:
            try:
                products = response.json()
                productGUIDs = JSONMozillaParser.JSONMozillaParser.parseGUIDs(products)
                response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?guid='+productGUIDs)
                if response.status_code == 200:
                    insertProducts = JSONMozillaParser.JSONMozillaParser.parseProducts(response.json())
                    newProducts = mozillaService.insertGroupProducts(insertProducts)
                    return JsonResponse(newProducts, safe=False,status=202)
                else:
                # En caso de error, devolver un mensaje de error
                    return JsonResponse({"error": "No se pudo obtener la informacion de los productos"}, response.status_code)
            except:
                return JsonResponse({"error": "No se pudo obtener las categorías"}, status=500)
        else:
            return JsonResponse({"error": "No se pudo obtener los productos"}, response.status_code)        
        
    def addProducts(request):
        data = json.loads(request.body)
        try:
            for product in data:
                mozillaRepository.insertSingleProduct(product)
            return JsonResponse({'message': 'Producto insertado correctamente'}, safe=False, status=201)
        except:
            return JsonResponse({'error': 'Error al insertar el producto'}, safe=False, status=500)
        
    def deleteProduct(request, productId):
        try:
            mozillaRepository.deleteProduct(productId)
            return JsonResponse({'message': 'Producto eliminado correctamente'}, safe=False, status=204)
        except:
            return JsonResponse({'error': 'Error al eliminar el producto'}, safe=False, status=500)