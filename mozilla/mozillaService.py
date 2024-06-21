import os
import requests
import json
from django.http import JsonResponse
from . import MozillaParser
from MonitoringSoftwareMarketplaces.serviceInterface import serviceInterface
from MonitoringSoftwareMarketplaces.repository import Repository

MARKETPLACE = "mozilla"
class mozillaService(serviceInterface):
    
  
 
    
    def getCategories(request):
        cache = request.GET.get('cache')
        if(cache == "1"):
            try:
                categories = Repository.getCategories(MARKETPLACE)
                return JsonResponse(categories, safe=False,status=200)
            except:
                return JsonResponse({"error": "No se pudo obtener las categorías"}, status=500)
        else:
            try:
                response = requests.get('https://addons.mozilla.org/api/v5/addons/categories/')
                if response.status_code == 200:
                    Repository.insertCategoriesM(response.json())
                    return JsonResponse(response.json(), safe=False,status=202)
                else:
                # En caso de error, devolver un mensaje de error
                    return JsonResponse({"error": "No se pudo obtener las categorías"}, status=500)
            except:
                return JsonResponse({"error": "No se pudo obtener las categorías"}, status=500)
            
    def getKeywords(request):
        cache = request.GET.get('cache')
        if(cache == "1"):
            Keywords = Repository.getKeywords(MARKETPLACE)
            return JsonResponse(Keywords, safe=False,status=200)
        else:
            response = requests.get('https://addons.mozilla.org/api/v5/addons/tags/')
            data = response.json()
            if response.status_code == 200:
                tagsJson = Repository.insertKeywords(data,MARKETPLACE)
                return JsonResponse(tagsJson, safe=False,status=200)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener los Tags "}, status=500)
    
    def getProductsByCategory(request):
        #Obtenemos el valor de los parametros enviados
        cache = request.GET.get('cache')
        category = request.GET.get('category')
        type = request.GET.get('type')
        page = request.GET.get('page') or 1

        #Comprobamos si la categoria existe
        if(not Repository.existeCategory(category, MARKETPLACE)):
                return JsonResponse({"error": "La categoria introducida no existe"}, status=404)
        #Si se nos indica que se debe de usar cache se obtiene la informacion de la base de datos
        if(cache == "1"):
            try: 
                products = Repository.getProductByCategory(category, MARKETPLACE)
                return JsonResponse(products, safe=False,status=200)
            except:
                return JsonResponse({"error": "No se pudo obtener los productos"}, status=500)
        #si no se nos indica que se debe de usar cache se obtiene la informacion de la api
        else:
            try:    
                categoryInfo = Repository.getCategoryInfo(category, MARKETPLACE)
                response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?category={}&type={}&page={}'.format(categoryInfo["api_name"],type,page))
                if response.status_code == 200:
                    products = response.json()
                    products = MozillaParser.MozillaParser.parseProducts(products)
                    Repository.insertGroupProducts(products,MARKETPLACE)
                    return JsonResponse(products, safe=False,status=202)
                else:
                # En caso de error, devolver un mensaje de error
                    return JsonResponse({"error": "No se pudo obtener las categorías"}, response.status_code)
            except:
                return JsonResponse({"error": "Error en la comunicación con la API"}, status=500)
    
    def getProductsByKewyword(request):
        #Obtenemos el valor de los parametros enviados
        cache = request.GET.get('cache')
        keyword = request.GET.get('keyword')
        page = request.GET.get('page') or 1
        if(not Repository.existeKewyword(keyword, MARKETPLACE)):
            return JsonResponse({"error": "La categoria introducida no existe"}, status=500)
        if(cache == "1"):
            try:
             pruduct = Repository.getProductByKeyword(keyword,MARKETPLACE)
             return JsonResponse(pruduct, safe=False,status=200)
            except:
                return JsonResponse({"error": "No se pudo obtener los productos"}, status=500)
        #si no se nos indica que se debe de usar cache se obtiene la informacion de la api
        else:
            response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?tag='+keyword+"&page="+page)
            if response.status_code == 200:
                try:
                    products = MozillaParser.MozillaParser.parseProducts(response.json())
                    Repository.insertGroupProducts(products,MARKETPLACE)
                    return JsonResponse(products, safe=False,status=202)
                except:
                    return JsonResponse({"error": "Ha habido un problema al obtener los productos"}, status=500)
            else:
            # En caso de error, devolver un mensaje de error
                return JsonResponse({"error": "No se pudo obtener las categorías"}, response.status_code)

    def getProductById(request, productId):
        cache = request.GET.get('cache')
        if(cache == "1"):
            product = Repository.getProductById(productId, MARKETPLACE)
            if(product):
                return JsonResponse(product, safe=False,status=200)
            else:
                return JsonResponse({"error": "No se pudo encontrar el producto"}, status=400)
        else:
            try:    
                response = requests.get('https://addons.mozilla.org/api/v5/addons/addon/'+productId)
                if response.status_code == 200:
                    parsedProduct = MozillaParser.MozillaParser.parseSingleProduct(response.json())
                    Repository.insertSingleProduct(parsedProduct,MARKETPLACE)
                    return JsonResponse(parsedProduct, safe=False,status=202)
                else:
                # En caso de error, devolver un mensaje de error
                    return JsonResponse({"error": "No se pudo obtener el producto"}, response.status_code)
            except:   
                return JsonResponse({"error": "No se pudo obtener el producto"}, status=400)
    
    def getProductByQuery(request):
        cache = request.GET.get('cache')
        query = request.GET.get('query')
        page = request.GET.get('page')
        if(cache == "1"):
            try:
                products = Repository.getProductsByQuery(query,MARKETPLACE)
                if(products):
                    return JsonResponse(products, safe=False,status=200)
                else:
                    return JsonResponse({"error": "No se pudo obtener ningun producto para esta query"}, status=400)
            except:
                return JsonResponse({"error": "No se pudo obtener los productos"}, status=500)
        response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?q ='+query+"&page="+page)
        if (response.status_code == 200):
                try:
                    products = MozillaParser.MozillaParser.parseProducts(response.json())
                    Repository.insertGroupProducts(products,MARKETPLACE)
                    return JsonResponse(products, safe=False,status=200)
                except:
                    return JsonResponse({"error": "No se pudo obtener el producto"}, status=400)
        else:
        # En caso de error, devolver un mensaje de error
            return JsonResponse({"error": "No se pudo obtener el producto"}, status=400)
    
    def discoveryProdcuts(request):
        page = request.GET.get('page')
        response = requests.get('https://addons.mozilla.org/api/v5/discovery')
        if response.status_code == 200:
            try:
                products = response.json()
                productGUIDs = MozillaParser.MozillaParser.parseGUIDs(products)
                response = requests.get('https://addons.mozilla.org/api/v5/addons/search/?guid='+productGUIDs+"&page="+page)
                if response.status_code == 200:
                    products = MozillaParser.MozillaParser.parseProducts(response.json())
                    Repository.insertGroupProducts(products,MARKETPLACE)
                    return JsonResponse(products, safe=False,status=200)
                else:
                # En caso de error, devolver un mensaje de error
                    return JsonResponse({"error": "No se pudo obtener la informacion de los productos"}, response.status_code)
            except:
                return JsonResponse({"error": "No se pudo obtener los productos"}, status=500)
        else:
            return JsonResponse({"error": "Ha habido un error en la cominucacion con la API"}, response.status_code)        
        
    def addProducts(request):
        data = json.loads(request.body)
        try:
            for product in data:
                Repository.insertSingleProduct(product, MARKETPLACE)
            return JsonResponse({'message': 'Producto insertado correctamente'}, safe=False, status=201)
        except:
            return JsonResponse({'error': 'Error al insertar el producto'}, safe=False, status=500)
        
    def deleteProduct(request, productId):
        try:
            Repository.deleteProduct(productId, MARKETPLACE)
            return JsonResponse({'message': 'Producto eliminado correctamente'}, safe=False, status=204)
        except:
            return JsonResponse({'error': 'Error al eliminar el producto'}, safe=False, status=500)