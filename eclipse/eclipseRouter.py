from django.urls import path

from . import printer

urlpatterns = [
    path('eclipse/', printer.bienvenidoEclispe , name='index'),
    path('eclipse/retrieve-marketplaces-and-categories', printer.printCategories, name='categories'),
    path('eclipse/categories<int:pageNumber>', printer.printCategories, name='categories_with_page'),
    path('eclipse/markets/<int:market>/categories/<int:category>/products', printer.printProductsByMarketandCategory , name='products_by_marketplace_and_category'),
    path('eclipse/product/id/<int:nodeId>', printer.printproductByNodeID , name='products_by_nodeId'),
    path('eclipse/products/top-favorites', printer.printTopFavorites , name='top_favorite_products'),
    path('eclipse/search/products', printer.searchProduct , name='index'),
    path('eclipse/products/title', printer.printProductByTitle , name='index'),
]