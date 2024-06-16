import json
import requests
from django.http import JsonResponse

class serviceInterface:

    def getCategories(request):
        pass
    def getKeywords(request):
        pass
    def getProductsByCategory(request, market, category):
        pass
    def getProductById(request, nodeId):
        pass 
    def getProductByQuery(request):
        pass
    def addProducts(request):
        pass 
    def deleteProduct(request, id):
        pass  
    def getProductByKeyword(request,keyword):
        pass
    