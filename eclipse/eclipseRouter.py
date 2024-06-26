from django.urls import path

from .eclipseService import EclipseService

urlpatterns = [
    path('eclipse/retrieve-marketplaces-and-categories', EclipseService.getCategories , name='categories'),
    path('eclipse/retrieve-keywords', EclipseService.getKeywords , name='products_by_marketplace_and_category'),
    path('eclipse/product/keyword/<str:keyword>', EclipseService.getProductByKeyword , name='products_by_keyword'),
    path('eclipse/markets/<int:market>/categories/<int:category>/products', EclipseService.getProductsByCategory , name='products_by_marketplace_and_category'),
    path('eclipse/product/id/<int:nodeId>', EclipseService.getProductById , name='products_by_nodeId'),
    path('eclipse/products/top-favorites', EclipseService.getTopFavorites , name='top_favorite_products'),
    path('eclipse/search/products/<str:query>', EclipseService.getProductByQuery , name='products_bu_query'),
    path('eclipse/products/title', EclipseService.getProductByTitle , name='index'),
    path('eclipse/add-products', EclipseService.addProducts , name='add_products'),
    path('eclipse/delete/product/<int:id>', EclipseService.deleteProduct , name='delete_products'),

]