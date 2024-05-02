from django.urls import path

from . import printer

urlpatterns = [
    path('eclipse/', printer.bienvenidoEclispe , name='index'),
    path('eclipse/categories', printer.printCategories, name='categories'),
    path('eclipse/categories<int:pageNumber>', printer.printCategories, name='categories_with_page'),
    path('eclipse/product/market/category/<int:category>,<int:market>', printer.printProductsByMarketandCategory , name='products_by_marketplace_and_category'),
    path('eclipse/product/node/<int:nodeId>', printer.printproductByNodeID , name='products_by_nodeId'),
    path('eclipse/topFavorites', printer.printTopFavorites , name='top_favorite_products'),
    path('eclipse/', printer.bienvenidoEclispe , name='index'),
    path('eclipse/', printer.bienvenidoEclispe , name='index'),
]