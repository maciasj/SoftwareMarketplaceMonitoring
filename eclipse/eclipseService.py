import json
import requests
from django.http import JsonResponse
from . import EclipseJSONParser
from MonitoringSoftwareMarketplaces.serviceInterface import serviceInterface

class EclipseService(serviceInterface):
    def getEclipseCategoriesAndMarketplaces(request):
        pageNumber = request.GET.get('page_num') or 1
        params = {'page_num': pageNumber}  
        response = requests.get('https://marketplace.eclipse.org/api/p', params=params)

        info = response.text
        if response.status_code == 200:
            try:
                categories = EclipseJSONParser.EclipseJSONParser.extractCategories(response)
                markets = EclipseJSONParser.EclipseJSONParser.extractMarkets(response)
                # Aqui se deberian de meter en la base de datos 
                return response
            except json.JSONDecodeError:
                return {'error': 'Error al decodificar JSON en la respuesta'}
        else:
            # Si la respuesta no fue exitosa, regresar un mensaje de error con el código de estado
            return {'error': f'Solicitud no exitosa. Código de estado: {response.status_code}'}

    def getProductsByMarketplaceAndCategory(request,category, market):
        print("Categoria", category, " Marketplace " , market)
        pageNumber = request.GET.get('page_num') or 1
        params = {'page_num': pageNumber}  

        response = requests.get('https://marketplace.eclipse.org/taxonomy/term/{},{}/api/p'.format(category, market), params=params)
        if response.status_code == 200:
            try:
                products = EclipseJSONParser.EclipseJSONParser.extractProducts(response)
                print(products)
                return response
            except json.JSONDecodeError:
                return {'error': 'Error al decodificar JSON en la respuesta'}
        else:
            # Si la respuesta no fue exitosa, regresar un mensaje de error con el código de estado
            print( response.status_code)
            return {'error': f'Solicitud no exitosa. Código de estado: {response.status_code}'}

    def getProductById(request, nodeId):
        pageNumber = request.GET.get('page_num') or 1
        params = {'page_num': pageNumber}  

        response = requests.get('https://marketplace.eclipse.org/node/{}}/api/p'.format(nodeId), params=params)
        
        if response.status_code == 200:
            try:
                info = response.text
                return response
            except json.JSONDecodeError:
                return {'error': 'Error al decodificar JSON en la respuesta'}
        else:
            # Si la respuesta no fue exitosa, regresar un mensaje de error con el código de estado
            print( response.status_code)
            return {'error': f'Solicitud no exitosa. Código de estado: {response.status_code}'}
        
    def getProductByTitle(request, title):
        pageNumber = request.GET.get('page_num') or 1
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
            print( response.status_code)
            return {'error': f'Solicitud no exitosa. Código de estado: {response.status_code}'}
        
    def getTopFavorites(request):
        pageNumber = request.GET.get('page_num') or 1
        params = {'page_num': pageNumber}  

        response = requests.get('https://marketplace.eclipse.org/favorites/top/api/p', params=params)
        
        if response.status_code == 200:
            try:
                info = response.text
                return response
            except json.JSONDecodeError:
                return {'error': 'Error al decodificar JSON en la respuesta'}
        else:
            # Si la respuesta no fue exitosa, regresar un mensaje de error con el código de estado
            print( response.status_code)
            return {'error': f'Solicitud no exitosa. Código de estado: {response.status_code}'}
        
    def getProductByQuery(request, query):
        pageNumber = request.GET.get('page_num') or 1
        filters = request.GET.get('filters') 
        params = {'page_num': pageNumber}  

        response = requests.get('http://marketplace.eclipse.org/api/p/search/apachesolr_search/{}'.format(query), params=params)
        
        if response.status_code == 200:
            try:
                info = response.text
                return response
            except json.JSONDecodeError:
                return {'error': 'Error al decodificar JSON en la respuesta'}
        else:
            # Si la respuesta no fue exitosa, regresar un mensaje de error con el código de estado
            print( response.status_code)
            return {'error': f'Solicitud no exitosa. Código de estado: {response.status_code}'}