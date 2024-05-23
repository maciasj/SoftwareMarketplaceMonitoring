from django.urls import path

from .eclipseService import EclipseService

urlpatterns = [
    path('eclipse/retrieve-marketplaces-and-categories', EclipseService.getCategoriesMarketplace , name='categories'),
    path('eclipse/markets/<int:market>/categories/<int:category>/products', EclipseService.getProductsByMarketplaceAndCategory , name='products_by_marketplace_and_category'),
    path('eclipse/product/id/<int:nodeId>', EclipseService.getProductById , name='products_by_nodeId'),
    path('eclipse/products/top-favorites', EclipseService.getTopFavorites , name='top_favorite_products'),
    path('eclipse/search/products', EclipseService.getProductByQuery , name='index'),
    path('eclipse/products/title', EclipseService.getProductByTitle , name='index'),
]