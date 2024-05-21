from django.urls import path

from .mozillaController import mozillaController

urlpatterns = [
path('mozilla/test', mozillaController.test , name='index'),
    path('mozilla/retrieve-categories', mozillaController.getCategories , name='Categories available at Mozilla marketplace'),
    path('mozilla/retrieve-tags', mozillaController.getTags , name='Tags available at Mozilla marketplace'),
    path('mozilla/categories/products', mozillaController.getProductsByCategory , name='products_by_category'),
    path('mozilla/tags/products', mozillaController.discoveryProdcuts , name='top_favorite_products'),
    path('mozilla/product/id/<str:productId>', mozillaController.getProductById , name='products_by_nodeId'),
    path('mozilla/product/name/<str:name>', mozillaController.getProductByTitle , name='products_by_title'),
    path('mozilla/discovery/products', mozillaController.discoveryProdcuts , name='top_favorite_products'),
    path('mozilla/search/products', mozillaController.getProductByQuery , name='index'),
]

