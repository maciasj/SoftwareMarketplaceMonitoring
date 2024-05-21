from django.urls import path

from .eclipseController import EclipseController

urlpatterns = [
    path('eclipse/retrieve-marketplaces-and-categories', EclipseController.getCategoriesMarketplace , name='categories'),
    path('eclipse/markets/<int:market>/categories/<int:category>/products', EclipseController.getProductsByMarketplaceAndCategory , name='products_by_marketplace_and_category'),
    path('eclipse/product/id/<int:nodeId>', EclipseController.getProductById , name='products_by_nodeId'),
    path('eclipse/products/top-favorites', EclipseController.getTopFavorites , name='top_favorite_products'),
    path('eclipse/search/products', EclipseController.getProductByQuery , name='index'),
    path('eclipse/products/title', EclipseController.getProductByTitle , name='index'),
]