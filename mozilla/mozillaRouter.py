from django.urls import path

from .mozillaService import mozillaService

urlpatterns = [

    path('mozilla/retrieve-categories', mozillaService.getCategories , name='Categories available at Mozilla marketplace'),
    path('mozilla/retrieve-tags', mozillaService.getKeywords , name='Keywords available at Mozilla marketplace'),
    path('mozilla/categories/products', mozillaService.getProductsByCategory , name='products_by_category'),
    path('mozilla/kewywords/products', mozillaService.getProductsByKewyword , name='products_by_keyword'),
    path('mozilla/product/id/<str:productId>', mozillaService.getProductById , name='products_by_nodeId'),
    path('mozilla/discovery/products', mozillaService.discoveryProdcuts , name='discovery_products'),
    path('mozilla/search/products', mozillaService.getProductByQuery , name='products_by_query'),
    path('mozilla/add-products', mozillaService.addProducts , name='add_products'),
    path('mozilla/delete-product/<str:productId>', mozillaService.deleteProduct , name='delete_products'),
]

