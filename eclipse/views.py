from django.http import HttpResponse
from .eclipseService import getEclipseCategoriesAndMarketplaces

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def testGetIds(requests):
    return HttpResponse()