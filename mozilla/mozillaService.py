import json
import requests
from django.http import JsonResponse
from MonitoringSoftwareMarketplaces.serviceInterface import serviceInterface

class mozillaService(serviceInterface):
    def getProductById(request, id):
        response = requests.get('https://addons.mozilla.org/api/v5/addons/categories/')
        print(response)
        pass
    def getProductByTitle(request, id):
        """Load in the file for extracting text."""
        pass
    def getProductByQuery(request, id):
        """Load in the file for extracting text."""
        pass
    def getCategories(request):
        response = requests.get('https://addons.mozilla.org/api/v5/addons/categories/')
        print(response)
        pass 
