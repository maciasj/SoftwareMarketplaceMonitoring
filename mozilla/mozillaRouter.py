from django.urls import path

from .mozillaService import mozillaService

urlpatterns = [
path('mozilla/test', mozillaService.test , name='index'),
    path('mozilla/retrieve-categories', mozillaService.getCategories , name='Categories available at Mozilla marketplace'),
    path('mozilla/retrieve-tags', mozillaService.getTags , name='Tags available at Mozilla marketplace'),
    path('mozilla/categories/products', mozillaService.getProductsByCategory , name='products_by_category'),
    path('mozilla/tags/products', mozillaService.getProductsByTag , name='top_favorite_products'),
    path('mozilla/product/id/<str:productId>', mozillaService.getProductById , name='products_by_nodeId'),
    path('mozilla/product/name/<str:name>', mozillaService.getProductByTitle , name='products_by_title'),
    path('mozilla/discovery/products', mozillaService.discoveryProdcuts , name='top_favorite_products'),
    path('mozilla/search/products', mozillaService.getProductByQuery , name='index'),
]

