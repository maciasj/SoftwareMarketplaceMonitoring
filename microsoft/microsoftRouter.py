from django.urls import path

from .microsoftService import microsoftService

urlpatterns = [
    path('microsoft/add-categories', microsoftService.addCategories , name='Categories available at Mozilla marketplace'),
    path('microsoft/retrieve-categories', microsoftService.getCategories , name='Categories available at Mozilla marketplace'),
    path('microsoft/product/id/<str:id>', microsoftService.getProductById , name='products_by_nodeId'),
    path('microsoft/search/products/', microsoftService.searchProduct , name='index'),
    path('microsoft/add-product/', microsoftService.addProduct , name='index'),
    path('microsoft/delete/product/<str:id>', microsoftService.deleteProduct , name='index'),
]

