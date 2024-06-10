import json
import requests
from . import EclipseJSONParser
from django.http import JsonResponse
from MonitoringSoftwareMarketplaces.serviceInterface import serviceInterface
from . import eclipseReposiroty


class EclipseService(serviceInterface):

    def getCategoriesMarketplace(request):
        cache = request.GET.get('cache')
        pageNumber = request.GET.get('page_num') or 1
        params = {'page_num': pageNumber}  
        if(cache == "1"):
            categories = eclipseReposiroty.getCategories()
            markets = eclipseReposiroty.getMarkets()
            return JsonResponse({'categories': categories, 'markets': markets}, safe=False,status=200)
       
        response = requests.get('https://marketplace.eclipse.org/api/p', params=params)
        if response.status_code == 200:
            try:
                categories = EclipseJSONParser.EclipseJSONParser.parseCategories(response)
                eclipseReposiroty.insertCategories(categories)
                markets = EclipseJSONParser.EclipseJSONParser.parseMarkets(response)
                eclipseReposiroty.insertMarkets(markets)
                response.json = {'categories': categories, 'markets': markets}
                return JsonResponse(response.json, safe=False,status=202)
            except :
                return JsonResponse({'error': 'Error al obtener las Categorias'},status=response.status_code, safe=False )
            
        else:
            return JsonResponse({'error': 'Error en la comunicación con el serivicio'},status=response.status_code, safe=False)
        
    def getProductsByMarketplaceAndCategory(request, market, category):
        cache = request.GET.get('cache')
        pageNumber = request.GET.get('page_num') or 1
        params = {'page_num': pageNumber}  
        if(cache == "1"):
            products = eclipseReposiroty.getProductsByCategory(market, category)
            return JsonResponse(products, safe=False,status=200)
        # Si no se especifica el parámetro cache, o si es falso, se hace la petición a la API
        response = requests.get('https://marketplace.eclipse.org/taxonomy/term/{},{}/api/p'.format(category, market), params=params)
        if response.status_code == 200:
            try:
                products = EclipseJSONParser.EclipseJSONParser.parseProducts(response,"category")
                for product in products:
                    eclipseReposiroty.insertSingleProduct(product)
                return JsonResponse(products, safe=False,status=202)
            except:
                return JsonResponse({'error': 'Error al obtener los productis'},status=response.status_code)
        else:
           return JsonResponse({'error': f'Error en la comunicacion con el servicio.'}, status=response.status_code)

    def getProductById(request, nodeId):
        cache = request.GET.get('cache')
        pageNumber = request.GET.get('page_num') or 1
        params = {'page_num': pageNumber}  
        if(cache == "1"):
            try:
                product = eclipseReposiroty.getProductById(nodeId)
                return JsonResponse(product, safe=False,status=201)
            except:
                return JsonResponse({'error': 'Error al obtener el producto'},status=404)
        # Si no se especifica el parámetro cache, o si es falso, se hace la petición a la API
        response = requests.get('https://marketplace.eclipse.org/node/{}/api/p'.format(nodeId), params=params)
        if response.status_code == 200:
            try:
                info = response.text
                product = EclipseJSONParser.EclipseJSONParser.extractSingleProduct(response)
                eclipseReposiroty.insertSingleProduct(product)
                return JsonResponse(product, safe=False,status=202)
            except json.JSONDecodeError:
                return {'error': 'Error al decodificar JSON en la respuesta'}
        else:
            # Si la respuesta no fue exitosa, regresar un mensaje de error con el código de estado
            return {'error': f'Solicitud no exitosa. Código de estado: {response.status_code}'}

    #Eliminar porque no tiene sentido    
    def getProductByTitle(request):
        pageNumber = request.GET.get('page_num') or 1
        title = request.GET.get('title')
        params = {'page_num': pageNumber}  
        response = requests.get('https://marketplace.eclipse.org/content/{}'.format(title), params=params)
        
        if response.status_code == 200:
            try:
                info = response.text
                return response
            except json.JSONDecodeError:
                return {'error': 'Error al decodificar JSON en la respuesta'}
        else:
            # Si la respuesta no fue exitosa, regresar un mensaje de error con el código de estado
            return {'error': f'Solicitud no exitosa. Código de estado: {response.status_code}'}
        
    def getTopFavorites(request):
        pageNumber = request.GET.get('page_num') or 1
        params = {'page_num': pageNumber}  

        response = requests.get('https://marketplace.eclipse.org/favorites/top/api/p', params=params)
        
        if response.status_code == 200:
            try:
                products = EclipseJSONParser.EclipseJSONParser.parseProducts(response,"favorites")
                for product in products:
                    eclipseReposiroty.insertSingleProduct(product)
                return JsonResponse(products, safe=False,status=202)
            except json.JSONDecodeError:
                return {'error': 'Error al decodificar JSON en la respuesta'}
        else:
            # Si la respuesta no fue exitosa, regresar un mensaje de error con el código de estado
            return {'error': f'Solicitud no exitosa. Código de estado: {response.status_code}'}
        
    def getProductByQuery(request):
        cache = request.GET.get('cache')
        query = request.GET.get('query')
        parameters = request.GET.get('parameters')
        if(cache == "1"):
            products = eclipseReposiroty.getProductsByQuery(query)
            return JsonResponse(products, safe=False,status=201)
        response = requests.get('http://marketplace.eclipse.org/api/p/search/apachesolr_search/{}'.format(query)+"?{}".format(parameters))
        if response.status_code == 200:
            try:
                products = EclipseJSONParser.EclipseJSONParser.parseProducts(response,"search")
                for product in products:
                    eclipseReposiroty.insertSingleProduct(product)
                return JsonResponse(products, safe=False,status=202)
            except :
                return {'error': 'Error al obtener los productos'}
        else:
            # Si la respuesta no fue exitosa, regresar un mensaje de error con el código de estado
            return {'error': f'Solicitud no exitosa. Código de estado: {response.status_code}'}

    def addProducts(request):
        data = json.loads(request.body)
        try:
            for product in data:
                eclipseReposiroty.insertSingleProduct(product)
            return JsonResponse({'message': 'Producto insertado correctamente'}, safe=False, status=201)
        except:
            return JsonResponse({'error': 'Error al insertar el producto'}, safe=False, status=500)
        
    def deleteProduct(request, id):
        try:
            eclipseReposiroty.deleteProduct(id)
            return JsonResponse({'message': 'Producto eliminado correctamente'}, safe=False, status=204)
        except:
            return JsonResponse({'error': 'Error al eliminar el producto'}, safe=False, status=500)
        